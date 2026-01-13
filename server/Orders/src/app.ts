import express from "express";
import cors from "cors";
import morgan from "morgan";
import orderRoutes from "./routes/orderRoutes";
import { metricsMiddleware } from "./middleware/metricsMiddleware";
import { register } from "./metrics";

const app = express();

app.use(express.json());
app.use(cors());
app.use(morgan("dev"));

/* ✅ METRICS MIDDLEWARE FIRST */
app.use(metricsMiddleware);

/* Health */
app.get("/health", (_req, res) => {
  res.status(200).json({
    status: "healthy",
    service: "orders",
    timestamp: Date.now(),
  });
});

/* Routes */
app.use("/orders", orderRoutes);

/* Metrics endpoint */
app.get("/metrics", async (_req, res) => {
  res.setHeader("Content-Type", register.contentType);
  res.end(await register.metrics());
});

/* Fault */
app.get("/fault", (_req, res) => {
  if (Math.random() < 0.2) process.exit(1);
  res.send("Order Service stable ✅");
});

export default app;
