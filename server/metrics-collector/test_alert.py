#!/usr/bin/env python3
"""
test_alert.py — Verifies email alerting works end-to-end.
Run from server/metrics-collector/:
    python test_alert.py

Requires .env to be populated with valid SMTP credentials.
"""

import os
from dotenv import load_dotenv

# Load .env before importing alert_mailer so env vars are present
load_dotenv()

from alert_mailer import send_anomaly_alert
import time

print("=" * 60)
print("TEST 1 — Sending HARD_FAILURE alert (CRITICAL)")
print("=" * 60)
send_anomaly_alert(
    service="orders",
    anomaly_type="HARD_FAILURE",
    severity="CRITICAL",
    metrics={
        "timestamp": "2025-01-15T10:30:00Z",
        "container_running": False,
        "rps": "N/A",
        "error_rate": "N/A",
        "p95_latency": "N/A",
    },
    extra_context="Simulated container crash — test run",
)

time.sleep(2)  # let thread dispatch

print()
print("=" * 60)
print("TEST 2 — Sending ML_ANOMALY alert (HIGH)")
print("=" * 60)
send_anomaly_alert(
    service="payments",
    anomaly_type="ML_ANOMALY",
    severity="HIGH",
    metrics={
        "timestamp": "2025-01-15T10:30:05Z",
        "rps": 0.0023,
        "error_rate": 0.312,
        "p95_latency_sec": 1.847,
        "ml_score": "anomaly (-1)",
    },
    extra_context="IsolationForest flagged metrics as anomalous. Error rate spike detected.",
)

time.sleep(2)

print()
print("=" * 60)
print("TEST 3 — Duplicate suppression (same key, should be debounced)")
print("=" * 60)
send_anomaly_alert(
    service="orders",
    anomaly_type="HARD_FAILURE",
    severity="CRITICAL",
    metrics={"note": "should be debounced"},
)

time.sleep(3)  # wait for threads to finish
print()
print("Done. Check your inbox and logs above.")
print("If no email received, verify SMTP_USER/SMTP_PASS/ALERT_TO in .env")