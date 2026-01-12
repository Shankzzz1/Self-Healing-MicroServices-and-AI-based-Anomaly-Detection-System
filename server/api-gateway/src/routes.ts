import { Application } from "express";
import { createProxyMiddleware } from "http-proxy-middleware";

export const setupRoutes = (app: Application) => {
  app.use(
    "/auth",
    createProxyMiddleware({
      target: "http://authentication:3001",
      changeOrigin: true,
      pathRewrite: { "^/auth": "" }
    })
  );

  app.use(
    "/orders",
    createProxyMiddleware({
      target: "http://orders:3002",
      changeOrigin: true,
      pathRewrite: { "^/orders": "" }
    })
  );

  app.use(
    "/payment",
    createProxyMiddleware({
      target: "http://payments:3003",
      changeOrigin: true,
      pathRewrite: { "^/payment": "" }
    })
  );
};
