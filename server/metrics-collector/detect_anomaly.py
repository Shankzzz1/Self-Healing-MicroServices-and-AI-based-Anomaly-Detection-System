import pandas as pd
import joblib
import time
import subprocess

from rca import diagnose

from heal import (
    restart_service,
    scale_service,
    circuit_breaker,
    throttle_traffic
)


MODEL_PATH = "model/anomaly_model.pkl"
DATA_PATH = "data/metrics.csv"

SERVICE_NAME = "orders"

CHECK_INTERVAL = 2
COOLDOWN = 120

model = joblib.load(
    MODEL_PATH
)

last_healing = 0


# =====================================
# HARD FAILURE DETECTION
# =====================================
def is_service_running(
    service_name
):

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

        return (
            result.stdout.strip()
            == "true"
        )

    except Exception:

        return False


while True:

    now = time.time()

    try:

        # =====================================
        # 1. HARD FAILURE
        # =====================================
        if not is_service_running(
            SERVICE_NAME
        ):

            print(
                f"🚨 {SERVICE_NAME} crashed"
            )

            if (
                now - last_healing
                > COOLDOWN
            ):

                restart_service(
                    SERVICE_NAME
                )

                last_healing = now

            else:

                print(
                    "⏳ Cooldown active"
                )

            time.sleep(
                CHECK_INTERVAL
            )

            continue


        # =====================================
        # 2. SOFT FAILURE
        # =====================================
        df = pd.read_csv(
            DATA_PATH
        ).tail(1)


        if df.empty:

            print(
                "⚠️ Waiting for metrics"
            )

            time.sleep(
                CHECK_INTERVAL
            )

            continue


        features = df[
            [
                "rps",
                "error_rate",
                "p95_latency"
            ]
        ]


        prediction = model.predict(
            features
        )


        if prediction[0] == -1:

            metrics = df.to_dict(
                "records"
            )[0]


            print(
                "🚨 ANOMALY DETECTED",
                metrics
            )


            # ========================
            # RCA
            # ========================
            cause = diagnose(
                metrics
            )


            print(
                f"🧠 Root Cause: {cause}"
            )


            # ========================
            # COOLDOWN
            # ========================
            if (
                now - last_healing
                < COOLDOWN
            ):

                print(
                    "⏳ Cooldown active"
                )

                time.sleep(
                    CHECK_INTERVAL
                )

                continue


            # ========================
            # HEALING DECISION
            # ========================
            if (
                cause
                == "service_failure"
            ):

                restart_service(
                    SERVICE_NAME
                )


            elif (
                cause
                == "traffic_spike"
            ):

                scale_service()


            elif (
                cause
                == "dependency_issue"
            ):

                circuit_breaker()


            elif (
                cause
                == "traffic_drop"
            ):

                throttle_traffic()


            else:

                print(
                    "⚠️ Unknown cause"
                )


            last_healing = now


        else:

            print(
                "✅ Normal"
            )


    except Exception as e:

        print(
            "❌ Detection error:",
            e
        )


    time.sleep(
        CHECK_INTERVAL
    )