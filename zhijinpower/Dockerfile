FROM python:3.12-slim

# Umgebungsvariablen aus config.json
ENV MQTT_HOST=localhost
ENV MQTT_PORT=1883
ENV TOKEN=""
ENV MACHINE_ID=""

# System-Tools installieren
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Arbeitsverzeichnis
WORKDIR /app
COPY . /app

# Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Startskript
CMD ["python", "main.py"]
