import dotenv from "dotenv";
import app from "./app";
import connectDB from "./utils/db";

dotenv.config();

const PORT = process.env.PORT || 3003;

connectDB().then(() => {
  app.listen(PORT, () => console.log(`🚀 Payment service running on port ${PORT}`));
});
