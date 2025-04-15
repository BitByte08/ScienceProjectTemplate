import time
import paho.mqtt.client as mqtt
# MQTT 설정
mqtt_broker = "mqtt-broker"  # 컨테이너 이름 사용
mqtt_port = 1883
mqtt_keepalive = 60

# MQTT 클라이언트 생성
client = mqtt.Client()

# MQTT 연결 시도 (try-except로 재시도)
def connect_mqtt():
    try:
        print(f"Connecting to MQTT broker at {mqtt_broker}...")
        client.connect(mqtt_broker, mqtt_port, mqtt_keepalive)
        client.loop_start()
        print("Connected to MQTT broker!")
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")
        print("Retrying...")
        time.sleep(5)  # 5초 대기 후 재시도
        connect_mqtt()  # 재귀적으로 다시 시도

# 연결 시도
connect_mqtt()

# FastAPI와 관련된 코드 (여기서는 예시로만 빠르게 간단하게 실행)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",  # React 개발 서버 주소
]

# CORS 미들웨어 등록
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # 허용할 Origin
    allow_credentials=True,
    allow_methods=["*"],              # 모든 HTTP 메서드 허용
    allow_headers=["*"],              # 모든 헤더 허용
)

@app.get("/api")
def read_root():
    return {"message": "Hello, FastAPI is connected to MQTT!"}