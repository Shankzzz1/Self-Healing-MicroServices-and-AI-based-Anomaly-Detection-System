**Fleshing out Demonstrations and Setup**

I'm now detailing the project's practical demonstrations. The failure simulation is straightforward, but the Kubernetes auto-scaling needs careful explanation. I'll outline the setup, the trigger for the load anomaly, the expected horizontal scaling behavior, and the commands to observe the process in real-time. My goal is to make these demonstrations easily reproducible for any user exploring the project.


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

## 🚀 Problem Statement

In real-world distributed systems:

- Failures are inevitable
- Blind restarts cause downtime
- Manual intervention does not scale

### Goal

Build a system that can:

> Observe itself, detect failures, reason about them, and heal automatically.

Exactly how production **SRE / Platform Engineering systems** work.

---

## 🧩 High-Level Architecture
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
```
### 🔍 Core Components

#### 1️⃣ Microservices Layer
This system is composed of several independent services built with Node.js and Express, containerized with Docker.

**Services:**
*   **Authentication Service:** Manages user registration and login, issuing JWTs for secure access.
*   **Orders Service:** Handles order creation, retrieval, and cancellation. It is secured by JWT verification.
*   **Payments Service:** Integrates with Razorpay to process payments for orders.
*   **API Gateway:** A single entry point that routes incoming requests to the appropriate microservice.

Each service exposes standard endpoints for health checks (`/health`) and metrics (`/metrics`), along with a fault injection endpoint (`/fault`) to simulate failures.

#### 2️⃣ Observability
Observability is achieved using a Prometheus and Grafana stack.

*   **Prometheus:** Scrapes metrics endpoints exposed by each microservice and the API gateway. It collects data on:
    *   Requests Per Second (RPS)
    *   Error Rate (specifically for 5xx status codes)
    *   P95 Latency (request duration)
*   **Grafana:** Provides dashboards for visualizing the metrics collected by Prometheus, offering a real-time view of system health.

#### 🧠 AI-Based Anomaly Detection
A Python-based `metrics-collector` service continuously queries Prometheus for the latest metrics. These metrics are fed into a machine learning model to detect abnormal behavior.

*   **Algorithm:** Uses an **Isolation Forest** model, an unsupervised learning algorithm effective for anomaly detection.
*   **Training:** The model is trained on a `metrics.csv` dataset representing normal operational behavior (RPS, error rate, p95 latency).
*   **Detection:** The system detects anomalies such as:
    *   Sudden traffic drops
    *   Latency spikes
    *   Error rate bursts
    *   Service crashes (hard failures)

#### 🛠️ Healing Decision Engine
Unlike naive systems that always restart a failing service, this system implements intelligent self-healing.

*   **Hard Failure:** If a service container crashes, the `detect_anomaly.py` script identifies that the container is not running and triggers an immediate restart via the `heal.py` script.
*   **Soft Failure:** If the Isolation Forest model predicts an anomaly based on metrics (e.g., latency spike), it also triggers a restart.
*   **Cooldown Period:** A 120-second cooldown period prevents restart loops, ensuring stability.

### ⚡ Kubernetes Auto-Scaling
The architecture also demonstrates horizontal auto-scaling in response to increased load using Kubernetes.

*   **Components:**
    *   **Kubernetes Deployment:** Manages the `orders` service pods.
    *   **HorizontalPodAutoscaler (HPA):** Monitors CPU utilization of the `orders` pods.
    *   **Metrics Server:** Provides the resource metrics that the HPA uses to make scaling decisions.
*   **Live Demo Flow:**
    1.  A load test script (`k6`) generates a traffic spike.
    2.  The CPU utilization of the `orders` pod rises.
    3.  The HPA detects the overload (CPU utilization exceeds the target of 2%).
    4.  The HPA automatically scales the number of `orders` pods from 1 up to a maximum of 5 to handle the load, ensuring zero downtime.

## 📂 Project Structure
```
server/
├── api-gateway/
├── Orders/
├── Payments/
├── authentication/
│
├── monitoring/
│   ├── prometheus/
│
├── metrics-collector/
│   ├── collector.py
│   ├── train_model.py
│   ├── detect_anomaly.py
│   ├── heal.py
│   └── model/
│
├── k8s/
│   ├── orders-deployment.yaml
│   ├── orders-service.yaml
│   └── orders-hpa.yaml
│
└── docker-compose.yml
```
## ⚙️ Setup and Usage

### Prerequisites
*   [Docker](https://www.docker.com/products/docker-desktop/)
*   [Node.js](https://nodejs.org/)
*   [k6](https://k6.io/docs/getting-started/installation/) (for Kubernetes load testing)

### 1. Installation
Clone the repository:
```bash
git clone https://github.com/shankzzz1/Self-Healing-MicroServices-and-AI-based-Anomaly-Detection-System.git
cd Self-Healing-MicroServices-and-AI-based-Anomaly-Detection-System/server
```

### 2. Run with Docker
Start all services (microservices, Prometheus, Grafana, MongoDB) using Docker Compose.
```bash
docker compose up --build
```
To stop all services:
```bash
docker compose down -v
```

### 3. Monitoring
*   **Prometheus:** `http://localhost:9090`
*   **Grafana:** `http://localhost:3005` (Login: `admin` / `admin`)

### 4. AI Anomaly Detection & Self-Healing

1.  **Navigate to the Metrics Collector:**
    ```bash
    cd metrics-collector
    ```

2.  **Collect initial metrics data:**
    Run the collector for a few minutes to gather baseline data.
    ```bash
    python collector.py
    ```
    Stop the script (`Ctrl+C`) after a few minutes. This will populate `data/metrics.csv`.

3.  **Train the ML Model:**
    Use the collected data to train the Isolation Forest model.
    ```bash
    python train_model.py
    ```
    This will create `model/anomaly_model.pkl`.

4.  **Start Anomaly Detection & Healing:**
    This script will monitor metrics and perform healing actions.
    ```bash
    python detect_anomaly.py
    ```

### 5. Trigger a Failure
In a new terminal, send a request to the fault injection endpoint of the `orders` service.
```bash
curl http://localhost:3000/orders/fault
```
**Expected Output in the `detect_anomaly.py` terminal:**
```
🚨 ANOMALY DETECTED {'timestamp': '...', 'rps': ..., 'error_rate': ..., 'p95_latency': ...}
🔁 Restarting service: orders
✅ orders restarted successfully
```

### 6. Kubernetes Auto-Scaling Demo
1.  **Enable Kubernetes** in Docker Desktop.

2.  **Deploy the Orders Service to Kubernetes:**
    From the `server/` directory, apply the Kubernetes configuration files.
    ```bash
    kubectl apply -f k8s/
    ```

3.  **Monitor the Pods and HPA:**
    Open two separate terminals to watch the scaling in real-time.

    *Terminal 1:*
    ```bash
    kubectl get pods -w
    ```
    *Terminal 2:*
    ```bash
    kubectl get hpa -w
    ```

4.  **Generate Load:**
    Run the `k6` load test script to simulate a traffic spike.
    ```bash
    k6 run scripts/load-test.js
    ```

5.  **Observe Auto-Scaling:**
    Watch as the number of `orders` pods increases from 1 to handle the load, and the CPU utilization is reported by the HPA. The pod count will scale down once the load test is complete.

## 🚀 Future Enhancements
*   Service-specific ML models for more granular anomaly detection.
*   Automated Root Cause Analysis (RCA).
*   Integration of Reinforcement Learning for more advanced healing decisions.
*   Alerting via Slack or email notifications.
*   Implementation of multi-cluster failover strategies.
