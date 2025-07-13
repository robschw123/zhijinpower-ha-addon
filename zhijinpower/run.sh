#!/usr/bin/env bashio
TOKEN=$(bashio::config 'TOKEN')
MACHINE_ID=$(bashio::config 'MACHINE_ID')
MQTT_USER=$(bashio::config 'MQTT_USER')
MQTT_PASS=$(bashio::config 'MQTT_PASS')
export TOKEN MACHINE_ID MQTT_USER MQTT_PASS
exec python3 /app/main.py
