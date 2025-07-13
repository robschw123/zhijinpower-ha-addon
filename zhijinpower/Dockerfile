# 1. Build-Argument für Multi-Arch
ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base-python:3.12
FROM ${BUILD_FROM}

# 2. Feste Defaults (nur Fallback)
ENV TZ=Europe/Berlin

# 3. System-Tools installieren
RUN apt-get update \
 && apt-get install -y build-essential bash \
 && rm -rf /var/lib/apt/lists/*

# 4. Arbeitsverzeichnis setzen
WORKDIR /app

# 5. Python-Dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# 6. Quellcode & Startskript
COPY . /app
RUN chmod +x /app/run.sh

# 7. run.sh als Entrypoint
ENTRYPOINT ["/app/run.sh"]
