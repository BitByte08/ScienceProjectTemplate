import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mqtt_client import MQTTClient

app = FastAPI()
latest_data = {"topic": "", "value": ""}

def handle_mqtt_message(topic, payload):
    print(f"[FastAPI] 처리: {topic} -> {payload}")
    latest_data["topic"] = topic
    latest_data["value"] = payload

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    global mqtt
    mqtt = MQTTClient(
        broker_url="mqtt-broker",
        topic="client/#"
    )
    mqtt.set_message_handler(handle_mqtt_message)
    mqtt.start()
    mysql_client.connect()

@app.on_event("shutdown")
async def shutdown_event():
    mysql_client.close()

@app.get("/client/all")
def get_client_all():

@app.get("/data")
def get_data():
    return {"data":latest_data}