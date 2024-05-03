# READ ME

**NETWORK**

`docker network create my_network`

**CADWAS**

`sudo docker build -t server .`

`sudo docker run -p 8000:8000 -d --network=my_network server `

**NGINX**

`sudo docker build -t server_nginx .`

`sudo docker run -p 80:80 -d --network=my_network server_nginx`