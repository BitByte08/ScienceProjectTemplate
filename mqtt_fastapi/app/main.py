from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from fastapi import FastAPI
import pymysql
import paho.mqtt.client as mqtt
import asyncio

MQTT_BROKER = "mqtt-broker"  # 예시로 public MQTT 브로커 사용
MQTT_PORT = 1883
MQTT_TOPIC = "client/#"

MYSQL_HOST = "mysql"
MYSQL_USER = "root"
MYSQL_PASSWORD = "qwer"
MYSQL_DATABASE = "DB"

# MQTT 클라이언트 초기화
mqtt_client = mqtt.Client()

app = FastAPI()

def get_mysql_connection():
    return pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        cursorclass=pymysql.cursors.DictCursor
    )

def on_message(client, topic, msg):
    message =   str(msg.payload.decode('utf-8'))
    print(f'Received message: {message}')
    # 여기서 메시지를 적절히 처리할 수 있음 (예: 데이터베이스 저장, API 호출 등)
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            # JSON 메시지를 예시로 넣음 (메시지 형식에 맞게 처리 가능)
            data = json.loads(message)
            client_name = msg.topic.split('/')[1]
            cursor.execute("SELECT id FROM client WHERE client_name = %s", (client_name))
            result = cursor.fetchone()

            if not result:
                cursor.execute("INSERT INTO client(client_name) values (%s)", (client_name))
                connection.commit()
                cursor.execute("SELECT id FROM client WHERE client_name = %s", (client_name))
                result = cursor.fetchone()

            client_id = result['id']

            # 2. ldr_data 테이블에 데이터 삽입
            cursor.execute(
                "INSERT INTO ldr_data (id, brightness) VALUES (%s, %s)",
                (client_id, data['brightness'])
            )
            connection.commit()
            print(f"Inserted brightness {data['brightness']} for client '{client_name}' (id={client_id})")

    finally:
        connection.close()
    

# MQTT 클라이언트 연결
def connect_mqtt():
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
    mqtt_client.subscribe(MQTT_TOPIC)
    mqtt_client.loop_start() 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    # FastAPI 앱 시작 시 MQTT 연결을 설정
    connect_mqtt()

@app.get("/status")
async def get_status():
    # MQTT 클라이언트가 정상적으로 연결되었는지 상태 확인
    if mqtt_client.is_connected():
        return {"status": "Connected to MQTT broker"}
    else:
        return {"status": "Not connected to MQTT broker"}