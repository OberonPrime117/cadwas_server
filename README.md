## DOCKER

`sudo apt install docker.io`

`sudo apt install python3 python3-pip`

`python3 join.py`

**REMOVE**

`sudo docker stop $(sudo docker ps -aq)`

`sudo docker rm $(sudo docker ps -aq)`

`sudo docker rmi $(sudo docker images -aq)`

**CADWAS**

`sudo docker build -t server .`

`sudo docker run -p 8000:8000 -d --network=my_network --name server server `

**NETWORK**

`docker network create my_network`

**NGINX**

`sudo docker build -t server_nginx .`

`sudo docker run -p 80:80 -d --network=my_network server_nginx`