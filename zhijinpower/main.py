import time
import os
import json
from dotenv import load_dotenv
load_dotenv()

from api import get_mach_info
import paho.mqtt.publish as publish

from config import SENSORS, BINARY_SENSORS

DEVICE_ID = os.getenv("MACHINE_ID")
TOKEN = os.getenv("TOKEN")
MQTT_HOST = os.getenv("MQTT_HOST", "core-mosquitto")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
INTERVAL = 180  # 3 min
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASS = os.getenv("MQTT_PASS")


DISCOVERY_PREFIX = "homeassistant"  # Default-Base für Discovery
DISCOVERY_DEVICE = {
    "identifiers": ["zhijinpower_ha"],
    "manufacturer": "ZhijinPower",
    "model": "Solar Inverter",
    "name": "ZhijinPower HA Bridge"
}

TOPIC_BASE = "home/zhijin"
RAW_DUMP_FILE = "raw_data.log"

def publish_sensor(topic_suffix, value):
    topic = f"{TOPIC_BASE}/{topic_suffix}"
    auth = None
    if MQTT_USER and MQTT_PASS:
        auth = {'username': MQTT_USER, 'password': MQTT_PASS}
    try:
        publish.single(
            topic,
            payload=str(value),
            hostname=MQTT_HOST,
            port=MQTT_PORT,
            auth=auth,
            keepalive=60
        )
        print(f"[MQTT] {topic} → {value}")
        return True
    except Exception as e:
        print(f"[MQTT Error] Publish an {MQTT_HOST}:{MQTT_PORT} → {e}")
        return False

def dump_raw_data(data):
    """Hängt die rohe API-Antwort als JSON-Zeile an RAW_DUMP_FILE an."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    entry = {
        "time": timestamp,
        "device_id": DEVICE_ID,
        "data": data
    }
    with open(RAW_DUMP_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

def publish_discovery(host, port, auth=None):
    """
    Sendet MQTT-Discovery-Config für alle Sensoren.
    Muss einmal vor dem ersten publish_sensor-Aufruf aufgerufen werden.
    """
    for sensor in SENSORS:
        topic = (
            f"{DISCOVERY_PREFIX}/sensor/{sensor['object_id']}/config"
        )
        payload = {
            "name": sensor["name"],
            "state_topic": sensor["state_topic"],
            "unit_of_measurement": sensor.get("unit", None),
            "device_class": sensor["device_class"],
            "unique_id": sensor["object_id"],
            "device": DISCOVERY_DEVICE
        }
        publish.single(
            topic,
            json.dumps(payload),
            hostname=host,
            port=port,
            auth=auth,
            retain=True  # wichtig: Config dauerhaft behalten
        )
        print(f"[DISCOVERY] Published config for {sensor['name']}")

    # binary sensors
    for b in BINARY_SENSORS:
        topic = f"{DISCOVERY_PREFIX}/binary_sensor/{b['object_id']}/config"
        payload = {
            "name": b["name"],
            "state_topic": b["state_topic"],
            "payload_on": b["payload_on"],
            "payload_off": b["payload_off"],
            "device_class": b["device_class"],
            "unique_id": b["object_id"],
            "device": DISCOVERY_DEVICE,
        }
        publish.single(topic, json.dumps(payload), hostname=host, port=port, auth=auth, retain=True)
        
if __name__ == "__main__":
    # .env geladen, MQTT_HOST, MQTT_PORT, MQTT_USER, MQTT_PASS gesetzt
    auth = None
    if MQTT_USER and MQTT_PASS:
        auth = { "username": MQTT_USER, "password": MQTT_PASS }

    # 1x Discovery-Nachrichten senden
    publish_discovery(MQTT_HOST, MQTT_PORT, auth)
    
    while True:
        print(f"[Debug] Token={TOKEN} DEVICE_ID={DEVICE_ID}")
        if not TOKEN or not DEVICE_ID:
            print("[Warning] Missing environment variables!")

        data = get_mach_info(TOKEN, DEVICE_ID)
        dump_raw_data(data)    # Rohdaten sichern
    
        if data:
            try:
                publish_sensor("voltage", float(data["dianya"]["value"]))
                publish_sensor("current", float(data["cddl"]["value"]))
                publish_sensor("temperature", float(data["temperature"]["value"]))
                publish_sensor("energy_total", float(data["total_power"]["value"]))
                publish_sensor("discharge_current", float(data["fddl"]["value"]))
                publish_sensor("solar_active", "1" if int(data["solar_status"]["value"]) else "0")
                publish_sensor("load_active", "1" if int(data["work_status"]["value"]) else "0")
                publish_sensor("wind_active", "1" if int(data["power_status"]["value"]) else "0")
                print("[OK] Sensor values published.")
            except Exception as e:
                import traceback
                traceback.print_exc()
                print(f"[Parse Error] {e}")
        else:
            print("[Warning] No data received.")
    
        time.sleep(INTERVAL)
