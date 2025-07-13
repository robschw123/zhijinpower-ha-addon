# 1. Build-Argument für Multi-Arch
ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM ${BUILD_FROM}

# 2. Feste Defaults (nur Fallback)
ENV TZ=Europe/Berlin

# 3. System-Tools installieren
RUN apk update \
 && apk add --no-cache \
    bash \
    build-base \
    python3 \
    py3-pip \
 && ln -sf /usr/bin/python3 /usr/bin/python \
 && rm -rf /var/cache/apk/*
 
# 4. Arbeitsverzeichnis setzen
WORKDIR /app

# 5. Python-Dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# 6. Quellcode & Startskript
ARG CACHE_BREAKER
RUN echo "Cache breaker: $CACHE_BREAKER"
COPY . /app
RUN chmod +x /app/run.sh

# 7. run.sh als Entrypoint
ENTRYPOINT ["/app/run.sh"]
