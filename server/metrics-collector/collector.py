import requests
import time
import pandas as pd
import os
from datetime import datetime

PROM_URL = "http://localhost:9090/api/v1/query"

QUERIES = {
    "rps": 'sum(rate(http_requests_total[1m]))',
    "error_rate": 'sum(rate(http_requests_total{status=~"5.."}[1m]))',
    "p95_latency": 'histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[1m])) by (le))'
}

CSV_PATH = "data/metrics.csv"

def query_prometheus(query):
    res = requests.get(PROM_URL, params={"query": query})
    data = res.json()
    if data["status"] != "success" or not data["data"]["result"]:
        return 0
    return float(data["data"]["result"][0]["value"][1])

while True:
    row = {
        "timestamp": datetime.utcnow().isoformat(),
        "rps": query_prometheus(QUERIES["rps"]),
        "error_rate": query_prometheus(QUERIES["error_rate"]),
        "p95_latency": query_prometheus(QUERIES["p95_latency"]),
    }

    print(row)

    df = pd.DataFrame([row])
    write_header = not os.path.exists(CSV_PATH)
    df.to_csv(CSV_PATH, mode="a", header=write_header, index=False)

    time.sleep(30)
