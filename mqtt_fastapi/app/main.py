from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import json
from fastapi import FastAPI
import pymysql
import paho.mqtt.client as mqtt
from pydantic import BaseModel
import asyncio
import traceback

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
            cursor.execute("SELECT id FROM client WHERE client_name = %s", (client_name,))
            result = cursor.fetchone()

            if not result:
                return

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

@app.get("/api/light")
def get_latest_light(client: str = Query(...)):
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT ldr_data.id, ldr_data.brightness, ldr_data.time
                FROM ldr_data
                JOIN client ON ldr_data.id = client.id
                WHERE client.client_name = %s
                ORDER BY ldr_data.time DESC
                LIMIT 1
            """, (client,))
            row = cursor.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="No data found for the specified client")
            return row
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        connection.close()
from datetime import timedelta, datetime

@app.get("/api/light/history")
def get_light_history(client: str = Query(...)):
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT ldr_data.id, ldr_data.brightness, ldr_data.time
                FROM ldr_data
                JOIN client ON ldr_data.id = client.id
                WHERE client.client_name = %s
                ORDER BY ldr_data.time DESC
                LIMIT 10
            """, (client,))
            rows = cursor.fetchall()
            return rows
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        connection.close()


class ClientModel(BaseModel):
    client_name: str
@app.post("/api/client/add")
def add_client(client: ClientModel):
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
        # 중복 방지를 위해 이미 존재하는지 확인 (선택 사항)
            cursor.execute("SELECT * FROM client WHERE client_name = %s", (client.client_name,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="Client already exists")

            # 삽입
            cursor.execute("INSERT INTO client(client_name) VALUES (%s)", (client.client_name,))
            connection.commit()
            return {"message": f"Client '{client.client_name}' added successfully."}
    except Exception as e:
        traceback.print_exc()
        connection.rollback()
        raise HTTPException(status_code=500, detail="Failed to add client")
    finally:
        connection.close()

@app.delete("/api/client/delete/{client_name}")
def delete_client(client_name: str):
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
        # 존재 여부 확인
            print(client_name)
            cursor.execute("SELECT * FROM client WHERE client_name = %s", (client_name,))
            data = cursor.fetchone()
            if not data:
                raise HTTPException(status_code=404, detail="Client not found")
            cursor.execute("DELETE FROM ldr_data WHERE id = %s", (data["id"],))
            connection.commit()
            cursor.execute("DELETE FROM client WHERE client_name = %s", (client_name,))
            connection.commit()
            return {"message": f"Client '{client_name}' deleted successfully."}
    except Exception as e:
        traceback.print_exc()
        connection.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete client")
    finally:
        connection.close()

@app.get("/api/client/list")
def get_clients():
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, client_name FROM client ORDER BY id ASC")
            result = cursor.fetchall()
            return result
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Failed to retrieve client list")
    finally:
        connection.close()