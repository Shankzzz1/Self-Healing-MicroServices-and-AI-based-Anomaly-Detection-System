import pandas as pd
import joblib
import time

MODEL_PATH = "model/anomaly_model.pkl"
DATA_PATH = "data/metrics.csv"

model = joblib.load(MODEL_PATH)

while True:
    df = pd.read_csv(DATA_PATH).tail(1)
    features = df[["rps", "error_rate", "p95_latency"]]

    prediction = model.predict(features)

    if prediction[0] == -1:
        print("🚨 ANOMALY DETECTED", df.to_dict("records")[0])
    else:
        print("✅ Normal")

    time.sleep(30)
