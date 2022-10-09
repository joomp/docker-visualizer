# syntax=docker/dockerfile:1

FROM node:16.17-slim as build-stage
WORKDIR /app
ARG VUE_APP_BACKEND_URL

COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:1.20 as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
