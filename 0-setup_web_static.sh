#!/usr/bin/env bash
# This script sets up web servers for the deployment of web_static.

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    apt-get update
    apt-get install -y nginx
fi

# Create necessary folders
mkdir -p /data/web_static/releases/test
mkdir -p /data/web_static/shared

# Create fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

# Create or recreate symbolic link
rm -rf /data/web_static/current
ln -s /data/web_static/releases/test /data/web_static/current

# Give ownership of /data/ folder to ubuntu user and group
chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config_text="
server {
    listen 80;
    server_name _;

    location /hbnb_static {
        alias /data/web_static/current/;
        index index.html;
    }

    location /redirect_me {
        rewrite ^/redirect_me https://www.youtube.com permanent;
    }

    error_page 404 /404.html;
    location = /404.html {
        root /usr/share/nginx/html;
        internal;
    }
}
"
echo "$config_text" > /etc/nginx/sites-available/default

# Restart Nginx
service nginx restart

exit 0
