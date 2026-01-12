import express from "express";
import cors from "cors";
import morgan from "morgan";
import client from "prom-client";
import orderRoutes from "./routes/orderRoutes";
import { metricsMiddleware } from "./middleware/metricsMiddleware";
import metricsClient from "./metrics";

const app = express();

app.use(express.json());
app.use(cors());
app.use(morgan("dev"));

/* =========================
   Prometheus Metrics
========================= */
const collectDefaultMetrics = client.collectDefaultMetrics;
collectDefaultMetrics({ register: client.register });

export const orderCount = new client.Counter({
  name: "order_total_created",
  help: "Total number of created orders",
});

/* =========================
   Routes
========================= */
// app.get("/metrics", async (_, res) => {
//   res.set("Content-Type", client.register.contentType);
//   res.end(await client.register.metrics());
// });

// app.get("/health", (_, res) => {
//   res.status(200).json({
//     status: "healthy",
//     service: "orders",
//     timestamp: Date.now(),
//   });
// });

app.get ("/health", orderRoutes);

// Fault injection (for anomaly testing)
app.get("/fault", (_, res) => {
  if (Math.random() < 0.2) process.exit(1); // 20% crash
  res.send("Order Service stable ✅");
});

app.use("/orders", orderRoutes);
app.use(metricsMiddleware);

app.get("/metrics", async (_req, res) => {
  res.set("Content-Type", metricsClient.register.contentType);
  res.end(await metricsClient.register.metrics());
});

export default app;
