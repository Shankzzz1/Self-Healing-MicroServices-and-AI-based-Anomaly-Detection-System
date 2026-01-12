import express from "express";
import cors from "cors";
import morgan from "morgan";
import dotenv from "dotenv";
import paymentRoutes from "./routes/paymentRoutes";
import { errorHandler } from "./middleware/errorMiddleware";
import { metricsMiddleware } from "./middleware/metricsMiddleware";
import metricsClient from "./metrics";

dotenv.config();

const app = express();
app.use(express.json());
app.use(cors());
app.use(morgan("dev"));

app.get("/health", paymentRoutes);
app.use("/payments", paymentRoutes);
app.use(errorHandler);
app.use(metricsMiddleware);

app.get("/metrics", async (_req, res) => {
  res.set("Content-Type", metricsClient.register.contentType);
  res.end(await metricsClient.register.metrics());
});

export default app;
