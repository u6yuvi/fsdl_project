# first stage builds svelte frontend
FROM 18.10.0-alpine3.15 as build-stage
WORKDIR /app
COPY . .
RUN npm run build

# second stage copies only the static dist files to nginx html dir
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
RUN mkdir -p /usr/share/nginx/html/assets
COPY  --from=build-stage /app/dist/assets /usr/share/nginx/html/assets
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
