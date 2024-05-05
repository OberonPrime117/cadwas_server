##### **INITIAL SETUP**

`sudo apt install docker.io`

`sudo apt install python3 python3-pip`

`python3 join.py`

##### **REMOVE**

`sudo docker system prune`

`sudo docker system prune -a`

`sudo docker stop $(sudo docker ps -aq)`

`sudo docker rm $(sudo docker ps -aq)`

`sudo docker rmi $(sudo docker images -aq)`

##### **CERTIFICATE**

Generate a private key
`sudo openssl genrsa -out selfsigned.key 2048`

Generate a certificate signing request
`sudo openssl req -new -key selfsigned.key -out selfsigned.csr`

Generate a self-signed certificate
`sudo openssl x509 -req -days 365 -in selfsigned.csr -signkey selfsigned.key -out selfsigned.crt`

##### **CADWAS**

`sudo docker build -t server .`

`sudo docker run -p 8000:8000 -d --network=my_network --name server server `

##### **NETWORK**

`docker network create my_network`

##### **NGINX**

`sudo docker build -t server_nginx .`

`sudo docker run -p 80:80 -d --network=my_network server_nginx`