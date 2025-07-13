# 1) Build-Argument mit Fallback
ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM ${BUILD_FROM}

# 2) Feste Defaults (nur Fallback)
ENV TZ=Europe/Berlin

# 3) System-Tools installieren
RUN apk update \
 && apk add --no-cache \
    bash \
    build-base \
    python3 \
    py3-pip \
 && ln -sf /usr/bin/python3 /usr/bin/python \
 && rm -rf /var/cache/apk/*

RUN command -v bashio

# 4) Arbeitsverzeichnis
WORKDIR /app

# 5) Virtuelle Umgebung + Pip-Upgrade
RUN python3 -m venv /opt/venv \
 && /opt/venv/bin/pip install --no-cache-dir --upgrade pip

# 6) Abhängigkeiten installieren
COPY requirements.txt /app/requirements.txt
RUN /opt/venv/bin/pip install --no-cache-dir -r /app/requirements.txt

# 7) Venv ins PATH
ENV PATH="/opt/venv/bin:$PATH"

# 8) Cache-Breaker für deterministische Builds
ARG CACHE_BREAKER
RUN echo "Cache breaker: $CACHE_BREAKER"

# 9) Quellcode + Entrypunkt
COPY . /app
RUN chmod +x /app/run.sh
ENTRYPOINT ["/app/run.sh"]
