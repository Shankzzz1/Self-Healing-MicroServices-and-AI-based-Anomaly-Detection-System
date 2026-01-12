import express from "express";
import { createPayment, healthCheck, verifyPayment } from "../controller/paymentController";

const router = express.Router();

router.post("/create", createPayment);
router.post("/verify", verifyPayment);
router.get("/health", healthCheck);

export default router;
