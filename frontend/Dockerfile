# Use the official NGINX image as the base image
FROM nginx:latest

# Copy the HTML file to the NGINX default document root
COPY index.html /usr/share/nginx/html/
COPY test.html /usr/share/nginx/html/

COPY nginx.conf /etc/nginx/nginx.conf

# Expose the default NGINX port
EXPOSE 80

# Start NGINX when the container launches
CMD ["nginx", "-g", "daemon off;"]
