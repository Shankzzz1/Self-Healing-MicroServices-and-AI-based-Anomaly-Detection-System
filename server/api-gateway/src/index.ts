import express from "express";
import cors from "cors";
import { setupRoutes } from "./routes";
import { metricsMiddleware } from "./middleware/metricsMiddleware";
import metricsClient from "./metrics";

const app = express();

app.use(cors());
app.use(express.json());
app.use(metricsMiddleware);

app.get("/metrics", async (_req, res) => {
  res.set("Content-Type", metricsClient.register.contentType);
  res.end(await metricsClient.register.metrics());
});
setupRoutes(app);

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`API Gateway running on port ${PORT}`);
});
