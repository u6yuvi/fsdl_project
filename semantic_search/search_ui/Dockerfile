FROM nginx:alpine
COPY search_ui/dist/* /usr/share/nginx/html
RUN mkdir -p /usr/share/nginx/html/assets
COPY search_ui/dist/assets /usr/share/nginx/html/assets
