import time
import paho.mqtt.client as mqtt

class MQTTClient:
    def __init__(self, broker_url, broker_port=1883, topic="#"):
        self.broker_url = broker_url
        self.broker_port = broker_port
        self.topic = topic
        self.client = mqtt.Client()
        self.handler = None

        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("[MQTTClient] 연결 성공")
            client.subscribe(self.topic)
            print(f"[MQTTClient] 구독 중: {self.topic}")
        else:
            print(f"[MQTTClient] 연결 실패. 코드: {rc}")

    def _on_message(self, client, userdata, msg):
        payload = msg.payload.decode()
        print(f"[MQTTClient] 메시지 수신: {msg.topic} -> {payload}")
        if self.handler:
            self.handler(msg.topic, payload)

    def set_message_handler(self, handler_func):
        self.handler = handler_func

    def start(self):
        try:
            print(f"[MQTTClient] {self.broker_url}:{self.broker_port}에 연결 시도 중...")
            self.client.connect(self.broker_url, self.broker_port, 60)
            self.client.loop_start()
        except Exception as e:
            print(f"[MQTTClient] 연결 실패: {e}")
            print("[MQTTClient] 5초 후 재시도...")
            time.sleep(5)
            self.start()