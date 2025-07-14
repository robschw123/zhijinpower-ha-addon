# 1) Zentrale Topic-Basis
TOPIC_BASE = "home/zhijin"

# 2) Sensor-Definitionen
SENSORS = [
    {
        "object_id": "zhijin_status",
        "name": "Solar Bridge Status",
        "state_topic": f"{TOPIC_BASE}/status",
        "device_class": "enum",
    },
    {
        "object_id": "zhijin_lastupdate",
        "name": "Solar Last Update",
        # Achte hier auf das gleiche Topic wie in deinem Code:
        "state_topic": f"{TOPIC_BASE}/last_update",
        "device_class": "timestamp",
    },
    {
        "object_id": "zhijin_voltage",
        "name": "Solar Battery Voltage",
        "state_topic": f"{TOPIC_BASE}/voltage",
        "unit": "V",
        "device_class": "voltage",
    },
    {
        "object_id": "zhijin_current",
        "name": "Solar Charge Current",
        "state_topic": f"{TOPIC_BASE}/current",
        "unit": "A",
        "device_class": "current",
    },
    {
        "object_id": "zhijin_discharge_current",
        "name": "Solar Discharge Current",
        "state_topic": f"{TOPIC_BASE}/discharge_current",
        "unit": "A",
        "device_class": "current",
    },
    {
        "object_id": "zhijin_temperature",
        "name": "Solar Temperature",
        "state_topic": f"{TOPIC_BASE}/temperature",
        "unit": "°C",
        "device_class": "temperature",
    },
    {
        "object_id": "zhijin_energy_total",
        "name": "Solar Energy Total",
        "state_topic": f"{TOPIC_BASE}/energy_total",
        "unit": "Wh",
        "device_class": "energy",
    },
    {
        "object_id": "zhijin_battery_percent",             # <-- notwendig!
        "name": "Solar Battery Percent",
        "state_topic": f"{TOPIC_BASE}/battery_percent",   # <-- konsistent zum Publish
        "unit": "%",
        "device_class": "battery",
        "value_template": "{{ value|int }}"
    },
    {
        "object_id": "zhijin_battery_type",
        "name": "Solar Battery Type",
        "state_topic": f"{TOPIC_BASE}/battery_type",
        # Keine unit und keine device_class!
        # Wenn du willst, kannst du ein icon setzen:
        "icon": "mdi:car-battery"
    },
]

# 3) Binary-Sensoren
BINARY_SENSORS = [
    {
        "object_id": "zhijin_solar_active",
        "name": "Solar Active",
        "state_topic": f"{TOPIC_BASE}/solar_active",
        "payload_on": "1",
        "payload_off": "0",
        "device_class": "power",
    },
    {
        "object_id": "zhijin_load_active",
        "name": "Solar Load Active",
        "state_topic": f"{TOPIC_BASE}/load_active",
        "payload_on": "1",
        "payload_off": "0",
        "device_class": "power",
    },
    {
        "object_id": "zhijin_wind_active",
        "name": "Solar Wind Active",
        "state_topic": f"{TOPIC_BASE}/wind_active",
        "payload_on": "1",
        "payload_off": "0",
        "device_class": "power",
    },
]
