#!/usr/bin/env bash
# Sets up your web servers for the deployment of web_static
if [ ! "$(which nginx)" ]
then
	sudo apt-get update -y > /dev/null &&\
	sudo apt-get install nginx -y > /dev/null
fi

mkdir -p /data/web_static/{releases/test,shared,current}

HTML="<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>"

echo -e "$HTML" | sudo tee /data/web_static/releases/test/index.html > /dev/null

if [ "$(find -L /data/web_static -maxdepth 2 -name current -xtype l | wc -l )" -gt 0 ]
then
	rm -r /data/web_static/current
fi
ln -ns /data/web_static/releases/test /data/web_static/current

if [ ! "$(id -u ubuntu)" ]
then
	sudo adduser ubuntu
	sudo usermod -aG sudo,ubuntu ubuntu
fi
chown -R ubuntu:ubuntu /data/


SERVER_CONFIG="server {
        listen 80 default_server;
        listen [::]:80 default_server;
        
	location /current/ {
		alias  /data/web_static/current/;
		autoindex off;
	}
        index index.html index.htm index.nginx-debian.html;
        server_name _;
        rewrite ^/hbnb_static nicknyanjui.tech permanent;
}"

echo -e "$SERVER_CONFIG" | sudo tee /etc/nginx/sites-enabled/default | > /dev/null

sudo service nginx restart > /dev/null
exit 0
