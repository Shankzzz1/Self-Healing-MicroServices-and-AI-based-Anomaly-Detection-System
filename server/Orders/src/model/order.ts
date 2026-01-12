import mongoose, { Document, Schema } from "mongoose";

export interface IOrder extends Document {
  userId: string;
  items: { productId: string; quantity: number; price: number }[];
  totalAmount: number;
  status: "pending" | "confirmed" | "cancelled";
}

const orderSchema = new Schema<IOrder>(
  {
    userId: { type: String, required: true },
    items: [
      {
        productId: { type: String },
        quantity: { type: Number },
        price: { type: Number },
      },
    ],
    totalAmount: { type: Number, required: true },
    status: {
      type: String,
      enum: ["pending", "confirmed", "cancelled"],
      default: "pending",
    },
  },
  { timestamps: true }
);

export const Order = mongoose.model<IOrder>("Order", orderSchema);
