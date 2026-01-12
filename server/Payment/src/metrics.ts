import client from "prom-client";

const register = client.register;

// ❌ REMOVE duplicate metrics
register.clear();

// ✅ Run default metrics ONCE
client.collectDefaultMetrics({ register });

export const httpRequestDuration = new client.Histogram({
  name: "http_request_duration_seconds",
  help: "HTTP request latency",
  labelNames: ["method", "route", "status"],
  registers: [register],
});

export const requestCounter = new client.Counter({
  name: "http_requests_total",
  help: "Total HTTP requests",
  labelNames: ["method", "route", "status"],
  registers: [register],
});

export default client;
