"""
detect_anomaly.py — MODIFIED (email alerting added)
Changes marked with # ✉️ NEW
"""

import pandas as pd
import joblib
import time
import load_env  
import subprocess
from heal import restart_service
from alert_mailer import send_anomaly_alert  # ✉️ NEW

MODEL_PATH = "model/anomaly_model.pkl"
DATA_PATH = "data/metrics.csv"

SERVICE_NAME = "orders"

CHECK_INTERVAL = 2
COOLDOWN = 120

model = joblib.load(MODEL_PATH)

last_restart = 0


def is_service_running(service_name):
    try:
        result = subprocess.run(
            [
                "docker",
                "inspect",
                "-f",
                "{{.State.Running}}",
                service_name
            ],
            capture_output=True,
            text=True
        )
        return result.stdout.strip() == "true"

    except Exception:
        return False


while True:
    now = time.time()

    try:
        # =========================================
        # 1. HARD FAILURE DETECTION (INSTANT)
        # =========================================
        if not is_service_running(SERVICE_NAME):

            print(f"🚨 {SERVICE_NAME} container crashed!")

            # ✉️ NEW — fire alert immediately (debounce handled inside)
            send_anomaly_alert(
                service=SERVICE_NAME,
                anomaly_type="HARD_FAILURE",
                severity="CRITICAL",
                metrics={
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "container_running": False,
                    "rps": "N/A",
                    "error_rate": "N/A",
                    "p95_latency": "N/A",
                },
                extra_context=f"Container '{SERVICE_NAME}' is not running. Restart triggered.",
            )

            if now - last_restart > COOLDOWN:
                restart_service(SERVICE_NAME)
                last_restart = now
            else:
                print("⏳ Cooldown active")

            time.sleep(CHECK_INTERVAL)
            continue

        # =========================================
        # 2. SOFT FAILURE DETECTION (ML)
        # =========================================
        df = pd.read_csv(DATA_PATH).tail(1)

        if df.empty:
            print("⚠️ No metrics yet")
            time.sleep(CHECK_INTERVAL)
            continue

        features = df[["rps", "error_rate", "p95_latency"]]
        prediction = model.predict(features)

        if prediction[0] == -1:

            anomaly = df.to_dict("records")[0]
            print("🚨 ANOMALY DETECTED", anomaly)

            # ✉️ NEW — determine severity from metrics
            error_rate = float(anomaly.get("error_rate", 0))
            p95_latency = float(anomaly.get("p95_latency", 0))

            if error_rate > 0.5 or p95_latency > 2.0:
                severity = "CRITICAL"
            elif error_rate > 0.2 or p95_latency > 1.0:
                severity = "HIGH"
            else:
                severity = "MEDIUM"

            send_anomaly_alert(
                service=SERVICE_NAME,
                anomaly_type="ML_ANOMALY",
                severity=severity,
                metrics={
                    "timestamp": anomaly.get("timestamp", "N/A"),
                    "rps": round(float(anomaly.get("rps", 0)), 4),
                    "error_rate": round(error_rate, 4),
                    "p95_latency_sec": round(p95_latency, 4),
                    "ml_score": "anomaly (-1)",
                },
                extra_context=(
                    f"IsolationForest flagged this row as anomalous. "
                    f"Restart will be attempted if cooldown allows."
                ),
            )

            if now - last_restart > COOLDOWN:
                restart_service(SERVICE_NAME)
                last_restart = now
            else:
                print("⏳ Cooldown active")

        else:
            print("✅ Normal")

    except Exception as e:
        print("❌ Detection error:", e)

    time.sleep(CHECK_INTERVAL)