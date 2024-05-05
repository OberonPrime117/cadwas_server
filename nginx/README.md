run NGINX on ec2 instance itself (NOT ON DOCKER)

`sudo apt install nginx`

`sudo mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.old`

`sudo mv nginx.conf /etc/nginx/nginx.conf`

`sudo systemctl daemon-reload`

`sudo systemctl restart nginx.service`