import pandas as pd
import joblib
import time
from heal import restart_service

MODEL_PATH = "model/anomaly_model.pkl"
DATA_PATH = "data/metrics.csv"

SERVICE_NAME = "orders"
CHECK_INTERVAL = 30          # seconds
COOLDOWN = 120               # seconds (prevents restart loop)

model = joblib.load(MODEL_PATH)
last_restart = 0

while True:
    df = pd.read_csv(DATA_PATH).tail(1)

    features = df[["rps", "error_rate", "p95_latency"]]
    prediction = model.predict(features)

    if prediction[0] == -1:
        anomaly = df.to_dict("records")[0]
        print("🚨 ANOMALY DETECTED", anomaly)

        now = time.time()
        if now - last_restart > COOLDOWN:
            restart_service(SERVICE_NAME)
            last_restart = now
        else:
            print("⏳ Cooldown active, skipping restart")

    else:
        print("✅ Normal")

    time.sleep(CHECK_INTERVAL)
