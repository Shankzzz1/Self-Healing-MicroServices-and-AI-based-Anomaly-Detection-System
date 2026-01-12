import express from "express";
import { registerUser, loginUser, healthCheck } from "../controller/authcontroller";

const router = express.Router();

router.post("/register", registerUser);
router.get("/health", healthCheck);
router.post("/login", loginUser);

export default router;
