#!/bin/bash

docker network create app-network 2>/dev/null || true


docker run --name mysql -e MYSQL_ROOT_PASSWORD=qwer -e MYSQL_DATABASE=DB -p 3306:3306 --network app-network mysql:8.0
# broker
docker build -t mqtt-broker ./broker
docker rm -f mqtt-broker 2>/dev/null

# fastapi
docker build -t mqtt-fastapi ./mqtt_fastapi
docker rm -f mqtt-fastapi 2>/dev/null

# web (React)
docker build -t mqtt-web ./web
docker rm -f mqtt-web 2>/dev/null
docker run -d --name mqtt-web --network app-network -p 3000:3000 mqtt-web
docker run -d --name mqtt-broker --network app-network -p 1883:1883 mqtt-broker
docker run -d --name mqtt-fastapi -e MYSQL_HOST=mysql -e MYSQL_USER=root -e MYSQL_PASSWORD=qwer -e MYSQL_DATABASE=DB --network app-network -p 8000:8000 mqtt-fastapi


echo "✅ All containers (broker, fastapi, web) are running!"