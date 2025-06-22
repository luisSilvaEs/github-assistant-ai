# Dockerfile for Create React App (CRA)

FROM node:20

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .

# CRA uses port 3000 by default
EXPOSE 3000

# Start CRA in dev mode
CMD ["npm", "start"]
