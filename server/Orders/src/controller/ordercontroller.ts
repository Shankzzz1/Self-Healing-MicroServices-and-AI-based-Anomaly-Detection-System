import { Request, Response } from "express";
import { Order } from "../model/order";
import { AuthRequest } from "../middleware/authMiddleware";

export const createOrder = async (req: Request, res: Response) => {
  try {
    const { items, totalAmount, userId } = req.body;

    const order = await Order.create({
      userId: userId || "testUser123",
      items,
      totalAmount,
    });

    res.status(201).json(order);
  } catch (error: any) {
    console.error("Error creating order:", error.message);
    res.status(500).json({ error: "Failed to create order", details: error.message });
  }
};


export const getOrder = async (req: Request, res: Response) => {
  try {
    const order = await Order.findById(req.params.id);
    if (!order) return res.status(404).json({ error: "Order not found" });
    res.json(order);
  } catch (error) {
    res.status(500).json({ error: "Error fetching order" });
  }
};

export const getUserOrders = async (req: Request, res: Response) => {
  try {
    const orders = await Order.find({ userId: req.params.id });
    res.json(orders);
  } catch (error) {
    res.status(500).json({ error: "Error fetching user orders" });
  }
};

export const cancelOrder = async (req: Request, res: Response) => {
  try {
    const order = await Order.findByIdAndUpdate(
      req.params.id,
      { status: "cancelled" },
      { new: true }
    );
    if (!order) return res.status(404).json({ error: "Order not found" });
    res.json(order);
  } catch (error) {
    res.status(500).json({ error: "Error cancelling order" });
  }
};

export const healthCheck = (req: Request, res: Response) => {
  res.status(200).json({
    status: "UP",
    service: process.env.SERVICE_NAME,
    timestamp: new Date().toISOString(),
  });
};