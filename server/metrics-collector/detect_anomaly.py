import pandas as pd
import joblib
import time
import subprocess
from heal import restart_service

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

        features = df[
            ["rps", "error_rate", "p95_latency"]
        ]

        prediction = model.predict(features)

        if prediction[0] == -1:

            anomaly = df.to_dict("records")[0]

            print("🚨 ANOMALY DETECTED", anomaly)

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