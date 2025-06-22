# Use Node.js Alpine as a lightweight base image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy only package files first for caching
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm install

# Copy the rest of the app
COPY . .

# Expose Vite's default dev port
EXPOSE 5173

# Start Vite dev server
CMD ["npm", "run", "dev", "--", "--host"]