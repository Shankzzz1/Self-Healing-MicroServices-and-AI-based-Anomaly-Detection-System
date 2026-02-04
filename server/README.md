# 🧠 AI-Based Self-Healing Microservices System

A production-inspired **self-healing microservices architecture** that automatically detects anomalies using real-time metrics and applies **intelligent recovery actions** without human intervention.

This project demonstrates **how modern distributed systems detect failures, reason about them, and heal themselves** using observability + ML + automation.

---

## 🚀 Problem Statement

In real-world microservices:

- Failures are inevitable
- Blind restarts cause downtime
- Manual intervention does not scale

**Goal:**  
Build a system that can **observe itself, detect abnormal behavior, and recover automatically** — similar to how production SRE systems work.

---

## 🧩 High-Level Architecture

Client
↓
API Gateway
↓
┌─────────────┬─────────────┬─────────────┐
│ Orders MS │ Payments MS │ Auth MS │
└─────────────┴─────────────┴─────────────┘
↓
Prometheus (Metrics)
↓
Metrics Collector
↓
AI Anomaly Detection
↓
Healing Decision Engine
↓
Automated Recovery


---

## 🔍 Core Components

### 1️⃣ Microservices Layer
- Orders, Payments, Authentication services
- Each service exposes:
  - `/health`
  - `/metrics`
  - `/fault` (failure simulation)

### 2️⃣ Observability
- **Prometheus** scrapes live metrics
- **Grafana** visualizes latency, traffic, and errors

Metrics used:
- Requests per second (RPS)
- Error rate
- P95 latency

---

## 🧠 AI-Based Anomaly Detection

- Isolation Forest trained on **normal system behavior**
- Detects deviations in runtime metrics
- Works on **live Prometheus data**, not logs

Detected anomalies include:
- Sudden latency spikes
- Traffic drops
- Abnormal request patterns

> ML is used only for **detection**, not blind decision-making.

---

## 🛠️ Intelligent Healing Engine (Key Contribution)

Unlike naive systems that always restart services, this project introduces a **healing decision layer**.

### Healing strategies implemented:

| Scenario | Healing Action |
|--------|----------------|
Service crash | Restart container |
High latency, no errors | Traffic throttling |
High error rate | Circuit breaker |
Traffic spike | Auto-scaling (simulated) |

📌 The system **selects the least disruptive action first**, just like real production systems.

---

## 🔁 Automated Self-Healing Flow

1. Metrics collected from Prometheus
2. ML model detects anomaly
3. Decision engine evaluates system state
4. Healing action executed automatically
5. Cooldown prevents restart loops
6. Service stabilizes without manual intervention

---

## 🧪 Failure Demonstration

Trigger a failure:

```bash
curl http://localhost:3000/orders/fault
What happens:

API Gateway returns timeout

Metrics spike detected

Anomaly flagged by ML

Healing engine triggers recovery

Service comes back online automatically

📂 Project Structure
server/
├── api-gateway/
├── orders/
├── payments/
├── authentication/
├── monitoring/
│   ├── prometheus/
│   └── grafana/
├── metrics-collector/
│   ├── collector.py
│   ├── train_model.py
│   ├── detect_anomaly.py
│   ├── heal.py
│   └── model/
│       └── anomaly_model.pkl
└── docker-compose.yml
🧠 Why This Is NOT “Just Using Tools”
✔ ML is used for behavioral learning, not thresholds
✔ Healing logic is custom-designed, not built-in
✔ Decisions are explainable and extensible
✔ System reacts automatically — no manual scripts
✔ Mimics real SRE self-healing patterns

📌 Resume-Ready Highlights
Built an AI-based self-healing microservices system using live metrics

Implemented automated anomaly detection using Isolation Forest

Designed a healing decision engine beyond simple restarts

Applied real-world observability and resilience patterns

🎯 One-Line Interview Explanation
“I built a self-healing microservices system that analyzes live Prometheus metrics using ML and automatically applies the least disruptive recovery strategy instead of blindly restarting services.”

🚧 Future Enhancements
Service-specific ML models

Real auto-scaling with Kubernetes

Root Cause Analysis (RCA)

Reinforcement learning for healing decisions

Alerting via Slack / Email

🏁 Conclusion
This project demonstrates how modern distributed systems detect failures and recover autonomously, combining observability, ML, and intelligent automation — exactly how production systems are designed.