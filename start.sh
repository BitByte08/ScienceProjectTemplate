#!/bin/bash

docker network create mqtt-network 2>/dev/null || true

# broker
docker build -t mqtt-broker ./broker
docker rm -f mqtt-broker 2>/dev/null
docker run -d --name mqtt-broker --network mqtt-network -p 1883:1883 mqtt-broker

# fastapi
docker build -t mqtt-fastapi ./mqtt_fastapi
docker rm -f mqtt-fastapi 2>/dev/null
docker run -d --name mqtt-fastapi --network mqtt-network -p 8000:8000 mqtt-fastapi

# web (React)
docker build -t mqtt-web ./web
docker rm -f mqtt-web 2>/dev/null
docker run -d --name mqtt-web --network mqtt-network -p 3000:3000 mqtt-web

echo "✅ All containers (broker, fastapi, web) are running!"