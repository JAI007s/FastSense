import os
import json
import time
import threading
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from . import crud

load_dotenv()

MQTT_HOST = os.getenv("MQTT_HOST", "mqtt")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPICS = os.getenv("MQTT_TOPICS", "sensors/data1,sensors/data2").split(",")

DEFAULT_THRESHOLDS = {
    "temperature": 30.0,
    "humidity": 80.0,
    "voltage": 5.0,
    "pressure": 1015.0,
    "light": 800.0
}
try:
    THRESHOLDS = json.loads(os.getenv("THRESHOLDS_JSON", json.dumps(DEFAULT_THRESHOLDS)))
except Exception:
    THRESHOLDS = DEFAULT_THRESHOLDS

client = mqtt.Client(protocol=mqtt.MQTTv311)

MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
if MQTT_USERNAME:
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)


_connect_lock = threading.Lock()
_connected = False

def on_connect(c, userdata, flags, rc):
    global _connected
    if rc == 0:
        print("[mqtt] Connected to broker")
        _connected = True
        
        for t in MQTT_TOPICS:
            t = t.strip()
            if t:
                c.subscribe(t)
                print(f"[mqtt] Subscribed to topic: {t}")
    else:
        print(f"[mqtt] Connect returned result code: {rc}")

def on_disconnect(c, userdata, rc):
    global _connected
    _connected = False
    print(f"[mqtt] Disconnected with rc={rc}. Will attempt to reconnect...")

def on_message(c, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)
        print(f"[mqtt] Received on {msg.topic}: {data}")

        
        raw_id = crud.store_raw_data(data)
        if raw_id is None:
            print("[mqtt] Failed storing raw data, skipping threshold checks")
            return

        
        for key, threshold in THRESHOLDS.items():
            if key in data:
                try:
                    val = float(data[key])
                except Exception:
                    continue
                if val > float(threshold):
                    
                    crud.store_alert(raw_id, key, val, float(threshold))
    except json.JSONDecodeError:
        print("[mqtt] Received non-JSON payload, ignoring")
    except Exception as e:
        print(f"[mqtt] on_message error: {e}")

def _start_loop():
    global client
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    backoff = 1
    while True:
        try:
            print(f"[mqtt] Connecting to {MQTT_HOST}:{MQTT_PORT}")
            client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
            client.loop_forever(retry_first_connection=True)
        except Exception as e:
            print(f"[mqtt] Connection failed: {e}. Backing off {backoff}s")
            time.sleep(backoff)
            backoff = min(backoff * 2, 60)

def start_mqtt():
    
    thread = threading.Thread(target=_start_loop, daemon=True, name="mqtt-thread")
    thread.start()
