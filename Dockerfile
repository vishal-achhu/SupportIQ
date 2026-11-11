FROM node:22-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --omit=dev
COPY tsconfig.json ./
COPY src ./src
RUN npm install -D typescript @types/node @types/express
RUN npx tsc
EXPOSE 3000
CMD ["node","dist/server.js"]
