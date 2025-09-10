import paho.mqtt.client as mqtt
import time
import random
import json
import os

BROKER = os.getenv("MQTT_HOST", "mqtt")
PORT = int(os.getenv("MQTT_PORT", 1883))
TOPICS = os.getenv("SIM_TOPICS", "sensors/data1,sensors/data2").split(",")

client = mqtt.Client(protocol=mqtt.MQTTv311)


while True:
    try:
        client.connect(BROKER, PORT, 60)
        print("[simulator] Connected to MQTT broker")
        break
    except Exception as e:
        print(f"[simulator] Broker not ready ({e}), retrying in 2s...")
        time.sleep(2)

client.loop_start()

try:
    while True:
        payload = {
            "temperature": round(random.uniform(20, 40), 2),
            "humidity": round(random.uniform(40, 90), 2),
            "voltage": round(random.uniform(3, 6), 2),
            "pressure": round(random.uniform(1000, 1020), 2),
            "light": round(random.uniform(300, 900), 2)
        }
        for t in TOPICS:
            t = t.strip()
            if t:
                client.publish(t, json.dumps(payload))
                print(f"[simulator] Published to {t}: {payload}")
        time.sleep(5)
except KeyboardInterrupt:
    print("[simulator] Stopped by user")
finally:
    client.loop_stop()
    client.disconnect()