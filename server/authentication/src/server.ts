import dotenv from "dotenv";
import app from "./app";
import connectDB from "./utils/db";

dotenv.config();

const PORT = process.env.PORT || 3001;

connectDB().then(() => {
  app.listen(PORT, () => console.log(`🚀 Auth service running on port ${PORT}`));
});
