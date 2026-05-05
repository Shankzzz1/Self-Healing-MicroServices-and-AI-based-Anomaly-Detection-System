"""
alert_mailer.py — Production-grade async email alerter
Drop-in for server/metrics-collector/alert_mailer.py

Features:
- Async (ThreadPoolExecutor — no event loop required in sync detect loop)
- Rate-limiting / debounce per service+type (ALERT_COOLDOWN_SECONDS)
- Structured HTML + plain-text email
- SMTP via env-config (TLS or plain)
- Thread-safe last-alert tracker
"""

import os
import smtplib
import threading
import logging
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

logger = logging.getLogger("alert_mailer")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# ── Config from env ──────────────────────────────────────────────────────────
SMTP_HOST     = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT     = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER     = os.getenv("SMTP_USER", "")          # sender address
SMTP_PASS     = os.getenv("SMTP_PASS", "")          # app password / secret
SMTP_USE_TLS  = os.getenv("SMTP_USE_TLS", "true").lower() == "true"

ALERT_TO      = os.getenv("ALERT_TO", "")           # comma-separated recipients
ALERT_FROM    = os.getenv("ALERT_FROM", SMTP_USER)  # display sender

ALERT_COOLDOWN_SECONDS = int(os.getenv("ALERT_COOLDOWN_SECONDS", "300"))  # 5 min debounce

# ── Internal state ────────────────────────────────────────────────────────────
_last_alert: dict[str, float] = {}   # key: "service|anomaly_type"  value: unix ts
_lock = threading.Lock()
_executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="mailer")


# ── Public API ────────────────────────────────────────────────────────────────

def send_anomaly_alert(
    *,
    service: str,
    anomaly_type: str,           # e.g. "HARD_FAILURE" | "ML_ANOMALY"
    severity: str,               # "CRITICAL" | "HIGH" | "MEDIUM"
    metrics: dict,               # raw metrics snapshot
    extra_context: Optional[str] = None,
) -> None:
    """
    Non-blocking. Submits email to thread pool after debounce check.
    Call this from detect_anomaly.py wherever anomaly is confirmed.
    """
    if not SMTP_USER or not SMTP_PASS or not ALERT_TO:
        logger.warning("Email not configured — skipping alert (set SMTP_USER/SMTP_PASS/ALERT_TO)")
        return

    key = f"{service}|{anomaly_type}"
    now = _now_ts()

    with _lock:
        last = _last_alert.get(key, 0)
        if now - last < ALERT_COOLDOWN_SECONDS:
            remaining = int(ALERT_COOLDOWN_SECONDS - (now - last))
            logger.info(f"Alert debounced for '{key}' — {remaining}s remaining in cooldown")
            return
        _last_alert[key] = now

    payload = _build_payload(service, anomaly_type, severity, metrics, extra_context)
    _executor.submit(_send, payload)
    logger.info(f"Alert queued for '{key}' (severity={severity})")


# ── Builders ──────────────────────────────────────────────────────────────────

def _build_payload(service, anomaly_type, severity, metrics, extra_context):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    recipients = [r.strip() for r in ALERT_TO.split(",") if r.strip()]

    subject = f"[{severity}] Anomaly Detected — {service} ({anomaly_type})"

    plain = _plain_body(service, anomaly_type, severity, ts, metrics, extra_context)
    html  = _html_body(service, anomaly_type, severity, ts, metrics, extra_context)

    return {
        "subject": subject,
        "to": recipients,
        "plain": plain,
        "html": html,
    }


def _plain_body(service, anomaly_type, severity, ts, metrics, extra_context):
    lines = [
        f"=== ANOMALY ALERT ===",
        f"Service     : {service}",
        f"Type        : {anomaly_type}",
        f"Severity    : {severity}",
        f"Timestamp   : {ts}",
        f"",
        f"--- Metrics Snapshot ---",
    ]
    for k, v in metrics.items():
        lines.append(f"  {k}: {v}")
    if extra_context:
        lines += ["", f"Context: {extra_context}"]
    lines += ["", "--- Self-Healing System | Auto-Generated Alert ---"]
    return "\n".join(lines)


def _html_body(service, anomaly_type, severity, ts, metrics, extra_context):
    severity_color = {
        "CRITICAL": "#dc2626",
        "HIGH":     "#ea580c",
        "MEDIUM":   "#ca8a04",
    }.get(severity, "#6b7280")

    metrics_rows = "".join(
        f"<tr><td style='padding:4px 8px;font-weight:600;color:#374151'>{k}</td>"
        f"<td style='padding:4px 8px;font-family:monospace'>{v}</td></tr>"
        for k, v in metrics.items()
    )

    context_block = (
        f"<p style='margin-top:16px;padding:12px;background:#fef3c7;border-left:4px solid #f59e0b;"
        f"border-radius:4px'><strong>Context:</strong> {extra_context}</p>"
        if extra_context else ""
    )

    return f"""
<!DOCTYPE html>
<html>
<body style="font-family:Arial,sans-serif;background:#f3f4f6;margin:0;padding:20px">
  <div style="max-width:600px;margin:auto;background:#fff;border-radius:8px;overflow:hidden;
              box-shadow:0 2px 8px rgba(0,0,0,0.1)">
    
    <!-- Header -->
    <div style="background:{severity_color};padding:20px 24px">
      <h2 style="color:#fff;margin:0;font-size:18px">🚨 Anomaly Detected</h2>
      <p style="color:rgba(255,255,255,0.85);margin:4px 0 0;font-size:13px">{ts}</p>
    </div>
    
    <!-- Body -->
    <div style="padding:24px">
      <table style="width:100%;border-collapse:collapse;margin-bottom:16px">
        <tr>
          <td style="padding:8px;width:50%;background:#f9fafb;border-radius:6px;text-align:center">
            <div style="font-size:11px;color:#6b7280;text-transform:uppercase;letter-spacing:.05em">Service</div>
            <div style="font-size:20px;font-weight:700;color:#111827;margin-top:2px">{service}</div>
          </td>
          <td style="width:8px"></td>
          <td style="padding:8px;width:50%;background:#fef2f2;border-radius:6px;text-align:center">
            <div style="font-size:11px;color:#6b7280;text-transform:uppercase;letter-spacing:.05em">Type</div>
            <div style="font-size:16px;font-weight:700;color:{severity_color};margin-top:2px">{anomaly_type}</div>
          </td>
        </tr>
      </table>
      
      <h3 style="margin:0 0 8px;font-size:14px;color:#374151;text-transform:uppercase;
                  letter-spacing:.05em">Metrics Snapshot</h3>
      <table style="width:100%;border-collapse:collapse;background:#f9fafb;border-radius:6px;
                    overflow:hidden">
        {metrics_rows}
      </table>
      
      {context_block}
    </div>
    
    <!-- Footer -->
    <div style="padding:16px 24px;background:#f9fafb;border-top:1px solid #e5e7eb;
                font-size:12px;color:#9ca3af;text-align:center">
      Self-Healing Microservices — Automated Alert System
    </div>
  </div>
</body>
</html>
"""


# ── SMTP sender (runs in thread) ──────────────────────────────────────────────

def _send(payload: dict) -> None:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = payload["subject"]
    msg["From"]    = ALERT_FROM
    msg["To"]      = ", ".join(payload["to"])

    msg.attach(MIMEText(payload["plain"], "plain"))
    msg.attach(MIMEText(payload["html"],  "html"))

    try:
        if SMTP_USE_TLS:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10)
            server.ehlo()
            server.starttls()
        else:
            server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=10)
        
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(ALERT_FROM, payload["to"], msg.as_string())
        server.quit()
        logger.info(f"Alert sent → {payload['to']} | {payload['subject']}")

    except Exception as e:
        logger.error(f"Failed to send alert email: {e}")


def _now_ts() -> float:
    return datetime.now(timezone.utc).timestamp()