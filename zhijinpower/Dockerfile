# 1. Build-Argument für Multi-Arch außen definieren
ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base-python:3.12
FROM ${BUILD_FROM}

# 2. Nutze das HA-Basis-Image, das bashio schon mitbringt
FROM ${BUILD_FROM}

# 3. Feste Defaults (nur Backup, echte Werte kommen aus run.sh)
ENV TZ=Europe/Berlin

# 4. System-Tools installieren (bashio ist schon da, kein curl o.ä. nötig)
RUN apt-get update \
 && apt-get install -y build-essential \
 && rm -rf /var/lib/apt/lists/*

# 5. Arbeitsverzeichnis
WORKDIR /app

# 6. Abhängigkeiten installieren
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# 7. Quellcode & das Start-Skript
COPY . /app
RUN chmod +x /app/run.sh

# 8. Run-Script als Entrypoint
ENTRYPOINT ["/app/run.sh"]
