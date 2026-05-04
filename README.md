# 🧠 AI-Based Self-Healing Microservices System

A production-inspired **self-healing microservices architecture** that automatically detects anomalies using live metrics and applies **intelligent recovery actions** without human intervention.

This project demonstrates how modern distributed systems:

- Observe themselves
- Detect abnormal behavior
- Decide the best recovery action
- Heal automatically

using:

- Microservices
- Prometheus
- Grafana
- Machine Learning
- Docker
- Kubernetes

---

# 🚀 Problem Statement

In real-world distributed systems:

- Failures are inevitable
- Blind restarts cause downtime
- Manual intervention does not scale

### Goal

Build a system that can:

> Observe itself, detect failures, reason about them, and heal automatically.

Exactly how production **SRE / Platform Engineering systems** work.

---

# 🧩 High-Level Architecture

```


                Client
                   │
                   ▼
             API Gateway
                   │
                   ▼
┌──────────────────────────────────────────┐
│        Microservices Layer              │
│                                          │
│  Orders   Payments   Authentication      │
└──────────────────────────────────────────┘
                   │
                   ▼
             Prometheus
                   │
                   ▼
         Metrics Collector
                   │
                   ▼
      AI Anomaly Detection Engine
                   │
                   ▼
         Healing Decision Engine
                   │
                   ▼
         Automated Recovery

🔍 Core Components
1️⃣ Microservices Layer

Services:

Orders Service
Payments Service
Authentication Service

Each service exposes:

/health
/metrics
/fault
2️⃣ Observability

Using:

Prometheus
Grafana

Collected metrics:

Requests Per Second (RPS)
Error Rate
P95 Latency
🧠 AI-Based Anomaly Detection

Uses:

Isolation Forest

Model learns:

Normal traffic patterns
Latency behavior
Error behavior

Detects:

✅ Traffic drops
✅ Latency spikes
✅ Error bursts
✅ Service instability

🛠️ Healing Decision Engine

Unlike naive systems that always restart services, this system chooses the least disruptive recovery strategy.

Healing Strategies
Scenario	Healing Action
Service crash	Restart container
High latency	Traffic throttling
High error rate	Circuit breaker
Traffic spike	Kubernetes auto-scaling
🔁 Automated Self-Healing Flow
Prometheus metrics
↓
ML anomaly detection
↓
Decision engine
↓
Best healing action selected
↓
System recovers automatically
🧪 Live Failure Demonstration

Trigger crash:

curl http://localhost:3000/orders/fault

System behavior:

Gateway timeout
↓
Prometheus metrics spike
↓
ML detects anomaly
↓
Healing engine triggers restart
↓
Service becomes healthy again
⚡ Kubernetes Auto-Scaling

This project also demonstrates:

Load anomaly → Horizontal scaling

Using:

Kubernetes
Horizontal Pod Autoscaler
Metrics Server

Live demo:

Traffic spike
↓
CPU rises
↓
HPA detects overload
↓
Pods scale from 1 → 4
↓
Zero downtime
📂 Project Structure


server/
├── api-gateway/
├── orders/
├── payments/
├── authentication/
│
├── monitoring/
│   ├── prometheus/
│   └── grafana/
│
├── metrics-collector/
│   ├── collector.py
│   ├── train_model.py
│   ├── detect_anomaly.py
│   ├── heal.py
│   ├── load_test.py
│   └── model/
│
├── k8s/
│   ├── orders-deployment.yaml
│   ├── orders-service.yaml
│   └── orders-hpa.yaml
│
└── docker-compose.yml

⚙️ Installation
Clone
git clone <your-repo-url>
cd server
🐳 Run with Docker

Start services:

docker compose up --build

Check containers:

docker ps

Stop services:

docker compose down -v
📊 Run Monitoring

Prometheus:



http://localhost:9090


Grafana:



http://localhost:3005


Default login:



admin
admin

🧠 Train ML Model

Move to collector:

cd metrics-collector

Collect metrics:

python collector.py

Train model:

python train_model.py

Start anomaly detection:

python detect_anomaly.py
🧪 Trigger Failure
curl http://localhost:3000/orders/fault

Expected:

🚨 ANOMALY DETECTED
🔁 Restarting service
✅ Service recovered
☸️ Kubernetes Auto-Scaling Demo
Enable Kubernetes

Enable Kubernetes in Docker Desktop.

Deploy

From project root:

kubectl apply -f k8s/

Check pods:

kubectl get pods

Check HPA:

kubectl get hpa
Watch scaling

Terminal 1:

kubectl get pods -w

Terminal 2:

kubectl get hpa -w
Generate load

Terminal 3:

Using k6:

k6 run scripts/load-test.js

Expected:

orders pod count:
1 → 2 → 4
📌 Resume Highlights
Built AI-based self-healing microservices system
Designed custom healing decision engine
Implemented anomaly detection using Isolation Forest
Integrated Prometheus + Grafana observability
Built Kubernetes-based auto-scaling recovery
Sustained 1400+ requests/sec with zero downtime
🎯 One-Line Interview Explanation

“I built a self-healing microservices platform where live Prometheus metrics are analyzed using ML, and the system automatically chooses the least disruptive recovery action such as restart, circuit breaking, or horizontal scaling.”

🚀 Future Enhancements
Service-specific ML models
Root Cause Analysis
Reinforcement Learning healing
Slack / Email alerts
Multi-cluster failover
🏁 Conclusion

This project demonstrates how modern distributed systems:

Detect failures
Analyze runtime behavior
Make intelligent recovery decisions
Heal automatically

using observability + machine learning + automation.


This README now reflects your **actual working system**, including the Kubernetes scaling demo you just completed.