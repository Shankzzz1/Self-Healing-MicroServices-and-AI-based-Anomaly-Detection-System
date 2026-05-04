import dotenv from "dotenv";
import app from "./app";
import connectDB from "./utils/db";

dotenv.config();

const PORT = process.env.PORT || 3002;


async function startServer() {
  try {

    // =====================================
    // KUBERNETES DEMO MODE
    // =====================================
    if (process.env.K8S_DEMO === "true") {
      console.log("🚀 Kubernetes demo mode — skipping MongoDB");

    } else {
      await connectDB();
      console.log("✅ MongoDB connected for Orders Service");
    }

    app.listen(PORT, () => {
      console.log(`🚀 Orders service running on port ${PORT}`);
    });

  } catch (err) {
    console.error("❌ DB connection failed:", err);
    process.exit(1);
  }
}


startServer();