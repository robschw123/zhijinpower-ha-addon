# ZhijinPower HA Bridge

Publishes solar inverter data from ZhijinPower devices to Home Assistant via MQTT.

---

## Repository Structure

```text
.
├── zhijinpower/               
│   ├── config.json            # Add-on manifest
│   ├── Dockerfile             # Container build instructions
│   ├── run.sh                 # Entry-point script (uses bashio)
│   ├── requirements.txt       # Python dependencies
│   ├── main.py                # Hauptlogik zum Abfragen & Veröffentlichen
│   └── api.py                 # API-Wrapper für ZhijinPower-Kommunikation
├── .gitignore
└── README.md
```

---

## Features

- Automatische Abfrage von Solar-Daten per HTTP/HTTPS  
- Publiziert Messwerte (Spannung, Strom, Leistung, Energie, u.v.m.) per MQTT  
- Unterstützt Home Assistant MQTT Auto-Discovery  
- Konfigurierbar über das Supervisor-Frontend (Token, Device ID, MQTT-Zugang)  
- Läuft als eigenständiges Home Assistant Add-on  

---

## Installation

### Voraussetzungen

- Home Assistant OS oder Supervised mit aktivem Add-on-Store  
- Laufender MQTT-Broker erreichbar unter konfigurierbarem Host/Port  

### Add-on-Repository hinzufügen

1. Öffne Home Assistant UI → **Supervisor** → **Add-on-Store**.  
2. Klicke oben rechts auf die drei Punkte → **Repository neu laden** oder **Neues Repository hinzufügen**.  
3. Gib die URL deines GitHub-Repos ein:  
   ```
   https://github.com/robschw123/zhijinpower-ha-addon
   ```  

### Add-on installieren

1. Suche in der Liste nach **ZhijinPower HA Bridge**.  
2. Klicke **Installieren**.  
3. Warte, bis das Image gebaut wird (kann je nach Hardware einige Minuten dauern).  
4. Unter **Einstellungen** konfiguriere deine Parameter (siehe Nächster Abschnitt).  
5. Klicke **Start**, um das Add-on zu starten.  

---

## Konfiguration

Alle konfigurierbaren Werte findest du im Supervisor-Frontend unter **Einstellungen** des Add-ons. Sie werden in `/data/options.json` gespeichert.

| Option        | Typ    | Beschreibung                                    | Standard        |
|---------------|--------|-------------------------------------------------|-----------------|
| MQTT_HOST     | str    | Hostname oder IP des MQTT-Brokers               | localhost       |
| MQTT_PORT     | int    | Port des MQTT-Brokers                           | 1883            |
| MQTT_USER     | str    | MQTT-Benutzername (falls Authentifizierung)      | mqtt-user       |
| MQTT_PASS     | str    | MQTT-Passwort (falls Authentifizierung)         | mqtt-pass       |
| TOKEN         | str    | API-Token für ZhijinPower Cloud                 | abc-123         |
| MACHINE_ID    | str    | Geräte-ID deines ZhijinPower Inverters          | \<your_ID\>     |

---

## MQTT Auto-Discovery

Beim Start publiziert das Add-on für jede Kennzahl ein Discovery-Topic. Ein Beispiel für den “Last Update” Sensor:

```jsonc
{
  "name": "ZhijinPower Last Update",
  "state_topic": "zhijinpower/last_update",
  "device_class": "timestamp",
  "unique_id": "zhijinpower_last_update",
  "availability_topic": "zhijinpower/status"
}
```

Anschließend erscheinen die Sensoren automatisch in Home Assistant.

---

## Entwicklung & Bau

### Docker-Build-Argumente

- **BUILD_FROM**  
  Basis-Image (Standard: `ghcr.io/home-assistant/amd64-base:latest`)  
- **CACHE_BREAKER**  
  Zufalls- oder Zeitstempel, um den Build-Cache gezielt zu invalidieren  

Beispiel:

```shell
docker build \
  --build-arg BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest \
  --build-arg CACHE_BREAKER=$(date +%s) \
  -t zhijinpower-addon:dev .
```

### Lokaler Test

1. Baue das Image lokal (s. o.).  
2. Starte es mit gemapptem `/data` und Umgebungsvariablen:

   ```shell
   docker run -it --rm \
     -v $(pwd)/data:/data \
     -e TOKEN=abc-123 \
     -e MACHINE_ID=xyz \
     -e MQTT_HOST=localhost \
     -e MQTT_PORT=1883 \
     -e MQTT_USER=user \
     -e MQTT_PASS=pass \
     zhijinpower-addon:dev
   ```

3. Schau dir die Logs an und verifiziere MQTT-Messages mit `mosquitto_sub`.

---

## Troubleshooting

- **`bashio: No such file or directory`**  
  Nutze das HA-offizielle Base-Image oder stelle sicher, dass dein Build-From korrekt ist.  
- **Alpine-Fehler beim `pip install`**  
  Siehe Abschnitt “Virtuelle Umgebung anlegen” im Dockerfile.  
- **Keine Entitäten in HA**  
  1. MQTT-Broker-Logs prüfen (`mosquitto_sub -t "zhijinpower/#" -v`).  
  2. Discovery-Topics kontrollieren (`<discovery_prefix>/sensor/.../config`).  
  3. Datum im ISO-Format mit `device_class: timestamp`.  

---

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe [LICENSE](LICENSE) für Details.

---

## Contributing

1. Forke das Repository.  
2. Erstelle einen Branch (`git checkout -b feature/mein-feature`).  
3. Committe deine Änderungen (`git commit -am 'Add feature'`).  
4. Pushe den Branch (`git push origin feature/mein-feature`).  
5. Öffne einen Pull Request.  
