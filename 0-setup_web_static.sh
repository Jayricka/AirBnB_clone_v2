#!/usr/bin/env bash

if ! command -v nginx &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y nginx
fi

sudo mkdir -p /data/web_static/releases/test /data/web_static/shared
echo "<html><head></head><body>Holberton School</body></html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/

nginx_config="/etc/nginx/sites-available/default"
if [ -e "$nginx_config" ]; then
    sudo sed -i '/location \/ {/a \location /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n' "$nginx_config"
fi

sudo service nginx restart
exit 0
