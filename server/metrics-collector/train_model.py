import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

DATA_PATH = "data/metrics.csv"
MODEL_PATH = "model/anomaly_model.pkl"

os.makedirs("model", exist_ok=True)

df = pd.read_csv(DATA_PATH)

features = df[["rps", "error_rate", "p95_latency"]]

model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42
)

model.fit(features)

joblib.dump(model, MODEL_PATH)
print("✅ Anomaly model trained & saved")
