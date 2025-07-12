SENSORS = [
    {
        "name": "Solar Voltage",
        "state_topic": "home/zhijin/voltage",
        "unit": "V",
        "device_class": "voltage",
        "object_id": "zhijin_voltage"
    },
    {
        "name": "Solar Current",
        "state_topic": "home/zhijin/current",
        "unit": "A",
        "device_class": "current",
        "object_id": "zhijin_current"
    },
    {
        "name": "Solar Discharge Current",
        "state_topic": "home/zhijin/discharge_current",
        "unit": "A",
        "device_class": "current",
        "object_id": "zhijin_discharge_current"
    },
    {
        "name": "Solar Temperature",
        "state_topic": "home/zhijin/temperature",
        "unit": "°C",
        "device_class": "temperature",
        "object_id": "zhijin_temperature"
    },
    {
        "name": "Solar Energy Total",
        "state_topic": "home/zhijin/energy_total",
        "unit": "kWh",
        "device_class": "energy",
        "object_id": "zhijin_energy_total"
    },
]
BINARY_SENSORS = [
    {
        "name": "Solar Active",
        "state_topic": "home/zhijin/solar_active",
        "payload_on": "1",
        "payload_off": "0",
        "device_class": "power",
        "object_id": "zhijin_solar_active"
    },
    {
        "name": "Solar Load Active",
        "state_topic": "home/zhijin/load_active",
        "payload_on": "1",
        "payload_off": "0",
        "device_class": "power",
        "object_id": "zhijin_load_active"
    },
    {
        "name": "Solar Wind Active",
        "state_topic": "home/zhijin/wind_active",
        "payload_on": "1",
        "payload_off": "0",
        "device_class": "power",
        "object_id": "zhijin_wind_active"
    },
]
