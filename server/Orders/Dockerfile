FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install
RUN npm install -g typescript   # ✅ THIS IS THE KEY FIX

COPY . .

RUN tsc                         # ✅ Direct call now works

EXPOSE 3002
CMD ["node", "dist/server.js"]
