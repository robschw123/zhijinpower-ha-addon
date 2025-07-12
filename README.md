# ZhijinPower HA Bridge (Home Assistant Add-on)

Dieses Add-on verbindet die ZhijinPower-Solarstation mit Home Assistant via MQTT und stellt wichtige Sensordaten als Entitäten bereit.

## 🔧 Funktionen

- Automatischer Datenabruf über die Hersteller-API
- Status- und Zeit-Sensoren mit MQTT Discovery
- Fehlerhandling & Logging via MQTT
- Konfigurierbare Parameter (Token, Machine-ID, MQTT)

## 🛠️ Installation

1. Füge das Repository in Home Assistant hinzu:
  https://github.com/robschw123/zhijinpower-ha-addon

2. Installiere das Add-on über den Add-on-Store
3. Konfiguriere `TOKEN` und `MACHINE_ID` über das Add-on-Menü

## ⚙️ Konfiguration (config.json)

| Parameter      | Beschreibung                                  |
|----------------|-----------------------------------------------|
| `TOKEN`        | Dein API-Zugangstoken                         |
| `MACHINE_ID`   | Geräte-ID deiner Solaranlage (z. B. `14929`)  |
| `MQTT_HOST`    | MQTT-Broker (meist `localhost`)               |
| `MQTT_PORT`    | Port des MQTT-Brokers (`1883`)                |

Beispielwerte findest du in der Datei [`env.example`](./env.example).

## 📡 MQTT

Sensoren werden automatisch via MQTT Discovery eingebunden – es ist keine manuelle YAML-Konfiguration nötig.

## ❗️ Hinweis

Bitte ersetze alle Platzhalter wie `<TOKEN>` und `<MACHINE_ID>` mit deinen echten Werten. Halte Token stets geheim und nutze `.env` zur sicheren Speicherung.

---
