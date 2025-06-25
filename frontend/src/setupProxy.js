const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = function (app) {
  app.use(
    "/chat",
    createProxyMiddleware({
      target: "http://backend:8000", // use "http://localhost:8000" if not using Docker
      changeOrigin: true,
    })
  );
};
