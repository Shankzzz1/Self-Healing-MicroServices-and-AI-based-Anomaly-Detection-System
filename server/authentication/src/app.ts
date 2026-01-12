import express from "express";
import cors from "cors";
import morgan from "morgan";
import dotenv from "dotenv";
import authRoutes from "./routes/authRoutes";
import metricsClient from "./metrics";
import { metricsMiddleware } from "./middleware/metricsMiddleware";

dotenv.config();

const app = express();
app.use(express.json());
app.use(cors());
app.use(morgan("dev"));

// app.get("/health", (_, res) => res.json({ status: "healthy" }));
app.get("/health", authRoutes);
app.use("/auth", authRoutes);
app.use(metricsMiddleware);

app.get("/metrics", async (_req, res) => {
  res.set("Content-Type", metricsClient.register.contentType);
  res.end(await metricsClient.register.metrics());
});

export default app;
