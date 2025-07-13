import time
import datetime
import os
import json

from api import get_mach_info
import paho.mqtt.publish as mqtt_publish
from config import SENSORS, BINARY_SENSORS

# MQTT / Add-on Konfiguration
DEVICE_ID    = os.getenv("MACHINE_ID")
TOKEN        = os.getenv("TOKEN")
MQTT_HOST    = os.getenv("MQTT_HOST", "core-mosquitto")
MQTT_PORT    = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USER    = os.getenv("MQTT_USER")
MQTT_PASS    = os.getenv("MQTT_PASS")
INTERVAL     = 180  # Sekunden

TOPIC_BASE       = "zhijinpower"
DISCOVERY_PREFIX = "homeassistant"
DISCOVERY_DEVICE = {
    "identifiers": ["zhijinpower_ha"],
    "manufacturer": "ZhijinPower",
    "model": "Solar Inverter",
    "name": "ZhijinPower HA Bridge"
}

def get_auth():
    if MQTT_USER and MQTT_PASS:
        return {"username": MQTT_USER, "password": MQTT_PASS}
    return None

def publish_sensor(suffix, value):
    topic = f"{TOPIC_BASE}/{suffix}"
    try:
        mqtt_publish.single(
            topic,
            payload=str(value),
            hostname=MQTT_HOST,
            port=MQTT_PORT,
            auth=get_auth(),
            retain=True
        )
        print(f"[MQTT] {topic} → {value}")
        return True
    except Exception as e:
        print(f"[MQTT Error] {e}")
        return False

def publish_discovery():
    auth = get_auth()
    # normale Sensoren
    for s in SENSORS:
        topic = f"{DISCOVERY_PREFIX}/sensor/{s['object_id']}/config"
        payload = {
            "name":             s["name"],
            "state_topic":      s["state_topic"],
            "unit_of_measurement": s.get("unit"),
            "device_class":     s["device_class"],
            "unique_id":        s["object_id"],
            "device":           DISCOVERY_DEVICE
        }
        mqtt_publish.single(topic, json.dumps(payload),
                            hostname=MQTT_HOST, port=MQTT_PORT,
                            auth=auth, retain=True)
        print(f"[DISCOVERY] Sensor {s['object_id']}")

    # binary sensors
    for b in BINARY_SENSORS:
        topic = f"{DISCOVERY_PREFIX}/binary_sensor/{b['object_id']}/config"
        payload = {
            "name":         b["name"],
            "state_topic":  b["state_topic"],
            "payload_on":   b["payload_on"],
            "payload_off":  b["payload_off"],
            "device_class": b["device_class"],
            "unique_id":    b["object_id"],
            "device":       DISCOVERY_DEVICE
        }
        mqtt_publish.single(topic, json.dumps(payload),
                            hostname=MQTT_HOST, port=MQTT_PORT,
                            auth=auth, retain=True)
        print(f"[DISCOVERY] Binary {b['object_id']}")

def publish_status(message):
    try:
        mqtt_publish.single(
            f"{TOPIC_BASE}/status",
            payload=message,
            hostname=MQTT_HOST,
            port=MQTT_PORT,
            auth=get_auth(),
            retain=True
        )
        print(f"[STATUS] → {message}")
    except Exception as e:
        print(f"[STATUS ERROR] {e}")

def voltage_to_soc(voltage: float, battery_type: int) -> int:
    limits = {
        2: (11.8, 13.5),   # Gel
        1: (11.8, 13.0),   # Li-Ion
        6: (12.8, 14.6),   # LiFePO4
        3: (11.8, 13.0),   # Blei-Säure
    }
    low, high = limits.get(battery_type, (11.8, 13.0))
    soc = (voltage - low) / (high - low) * 100
    return max(0, min(100, int(soc)))

if __name__ == "__main__":
    # 1x Auto-Discovery
    publish_discovery()

    while True:
        data = get_mach_info(TOKEN, DEVICE_ID)

        if data is None:
            publish_status("error: API timeout")
        elif not data:
            publish_status("error: no data")
        else:
            try:
                # 10 bestehende Werte
                publish_sensor("voltage",           float(data["dianya"]["value"]))
                publish_sensor("current",           float(data["cddl"]["value"]))
                publish_sensor("temperature",       float(data["temperature"]["value"]))
                publish_sensor("energy_total",      float(data["total_power"]["value"]))
                publish_sensor("discharge_current", float(data["fddl"]["value"]))
                publish_sensor("solar_active",      "1" if int(data["solar_status"]["value"]) else "0")
                publish_sensor("load_active",       "1" if int(data["work_status"]["value"])  else "0")
                publish_sensor("wind_active",       "1" if int(data["power_status"]["value"]) else "0")
                now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
                publish_sensor("last_update",       now_iso)

                # 11. Batterie-Prozent
                voltage = float(data["dianya"]["value"])
                btype   = int(data["battery_type"]["value"])
                percent = voltage_to_soc(voltage, btype)
                publish_sensor("battery_percent", percent)

                publish_status("success")

            except Exception as e:
                print(f"[EXCEPTION] {e}")
                publish_status(f"error:{e}")

        time.sleep(INTERVAL)
