import { Request, Response } from "express";
import Razorpay from "razorpay";
import crypto from "crypto";
import { Payment } from "../model/payment";
import dotenv from "dotenv";
dotenv.config();


const razorpay = new Razorpay({
  key_id: process.env.RAZORPAY_KEY_ID!,
  key_secret: process.env.RAZORPAY_KEY_SECRET!,
});

export const createPayment = async (req: Request, res: Response) => {
  try {
    console.log("Creating Razorpay order with:", req.body);
    console.log("Using keys:", process.env.RAZORPAY_KEY_ID, process.env.RAZORPAY_KEY_SECRET ? "✅ Secret loaded" : "❌ Missing secret");

    const options = {
      amount: req.body.amount * 100, // amount in paise
      currency: req.body.currency,
      receipt: req.body.receipt,
    };

    const order = await razorpay.orders.create(options);
    console.log("✅ Razorpay order created:", order);
    res.status(200).json(order);
  } catch (error: any) {
    console.error("❌ Razorpay Error:", error);
    res.status(500).json({
      error: "Failed to create Razorpay order",
      details: error.message,
    });
  }
};


// Verify Payment
export const verifyPayment = async (req: Request, res: Response) => {
  try {
    const { razorpay_order_id, razorpay_payment_id, razorpay_signature } = req.body;

    const body = razorpay_order_id + "|" + razorpay_payment_id;
    const expectedSignature = crypto
      .createHmac("sha256", process.env.RAZORPAY_KEY_SECRET!)
      .update(body.toString())
      .digest("hex");

    const isAuthentic = expectedSignature === razorpay_signature;

    if (isAuthentic) {
      await Payment.findOneAndUpdate(
        { razorpayOrderId: razorpay_order_id },
        {
          status: "success",
          razorpayPaymentId: razorpay_payment_id,
          razorpaySignature: razorpay_signature,
        }
      );
      res.status(200).json({ success: true, message: "Payment verified successfully" });
    } else {
      await Payment.findOneAndUpdate(
        { razorpayOrderId: razorpay_order_id },
        { status: "failed" }
      );
      res.status(400).json({ success: false, message: "Invalid signature" });
    }
  } catch (error) {
    console.error("Error verifying payment:", error);
    res.status(500).json({ error: "Payment verification failed" });
  }
};

export const healthCheck = (req: Request, res: Response) => {
  res.status(200).json({
    status: "UP",
    service: process.env.SERVICE_NAME,
    timestamp: new Date().toISOString(),
  });
};