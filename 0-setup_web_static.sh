#!/usr/bin/env bash
# Sets up your web servers for the deployment of web_static
if [ ! "$(which nginx)" ]
then
	sudo apt-get update -y > /dev/null 2>&1 &&\
	sudo apt-get install nginx -y > /dev/null 2>&1
fi

mkdir -p /data/web_static/{releases/test,shared,current}

HTML="<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>"
echo -e "$HTML" | sudo tee /data/web_static/releases/test/index.html > /dev/null 2>&1

if [ "$(find -L /data/web_static -maxdepth 1 -name current -xtype l | wc -l )" -gt 0 ]
then
	unlink /data/web_static/current
fi
ln -ns /data/web_static/releases/test /data/web_static/current

if [ ! "$(id -u ubuntu)" ]
then
	sudo adduser ubuntu
	sudo usermod -aG sudo,ubuntu ubuntu
fi
chown -R ubuntu:ubuntu /data/
SERVER_CONFIG=\
"server {
        listen 80 default_server;
        listen [::]:80 default_server;
        listen 443 default_server;
        listen [::]:443 default_server;
        server_name _;

        root /var/www/html;
        index index.html index.htm index.nginx-debian.html;
        try_files $uri $uri/ /index.html;

        location /hbnb_static/ {
                alias /var/www/static/;
                index index.html index.htm index.nginx-debian.html;
                try_files $uri $uri/ /hbnb_static/index.html;
        }

        rewrite ^/redirect_me https://github.com/n1klaus permanent;
        error_page 400 401 402 403 404 /40x.html;
        error_page 500 502 503 504 /50x.html;
        add_header X-Served-By $HOSTNAME;
        ignore_invalid_headers on;
}"
echo -e "$SERVER_CONFIG" | sudo tee /etc/nginx/sites-enabled/default > /dev/null 2>&1

sudo nginx -t > /dev/null 2>&1 &&\
sudo nginx -s reload > /dev/null 2>&1
exit 0
