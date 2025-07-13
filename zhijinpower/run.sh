#!/usr/bin/env bashio
set -e

# Konfigurationswerte importieren
TOKEN=$(bashio::config 'TOKEN')
MACHINE_ID=$(bashio::config 'MACHINE_ID')
MQTT_HOST=$(bashio::config 'MQTT_HOST')
MQTT_PORT=$(bashio::config 'MQTT_PORT')
MQTT_USER=$(bashio::config 'MQTT_USER')
MQTT_PASS=$(bashio::config 'MQTT_PASS')

# In die Environment exportieren
export TOKEN MACHINE_ID MQTT_HOST MQTT_PORT MQTT_USER MQTT_PASS

echo "Starting ZhijinPower Bridge with TOKEN: ${TOKEN}"

exec python3 /app/main.py
