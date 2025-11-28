import paho.mqtt.client as mqtt
import json
import time

class MQTTService:
    def __init__(self):
        self.client = mqtt.Client()
        self.mqtt_server = "172.20.10.3"
        self.mqtt_port = 1883
        self.control_topic = "control/topic"
        self.data_topic = "test/topics"
        
        # Variable para almacenar la última lectura del ESP32
        self.last_reading = {"peso": 0.0, "temperatura": 0.0}

        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect

    def on_connect(self, client, userdata, flags, rc):
        print(f"Conectado a MQTT. Código: {rc}")
        client.subscribe(self.data_topic)

    def on_message(self, client, userdata, msg):
        try:
            # Asumimos que el ESP32 envía JSON: {"peso": 150.5, "temperatura": 24.0}
            payload = msg.payload.decode()
            data = json.loads(payload)
            
            self.last_reading = data # Guardamos en memoria
            print(f"Dato actualizado desde ESP32: {self.last_reading}")
            
        except Exception as e:
            print(f"Error decodificando mensaje MQTT: {e}")

    def start(self):
        try:
            self.client.connect(self.mqtt_server, self.mqtt_port, 60)
            self.client.loop_start()
        except Exception as e:
            print(f"Error conexión MQTT: {e}")

    def send_command(self, command: str):
        self.client.publish(self.control_topic, command)

    # Método para que la API obtenga el dato actual
    def get_latest_data(self):
        return self.last_reading

mqtt_client = MQTTService()