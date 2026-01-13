import express from "express";
import cors from "cors";
import morgan from "morgan";
import dotenv from "dotenv";
import authRoutes from "./routes/authRoutes";
import { metricsMiddleware } from "./middleware/metricsMiddleware";
import { register } from "./metrics";

dotenv.config();

const app = express();
app.use(express.json());
app.use(cors());
app.use(morgan("dev"));

app.use(metricsMiddleware);
// app.get("/health", (_, res) => res.json({ status: "healthy" }));
app.get("/health", authRoutes);
app.use("/auth", authRoutes);

app.get("/metrics", async (_req, res) => {
  res.set("Content-Type", register.contentType);
  res.end(await register.metrics());
});

export default app;
