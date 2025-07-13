FROM python:3.12-slim

# (Optional) Feste Defaults als Fallback
ENV TZ=Europe/Berlin

# System-Tools installieren
RUN apt-get update \
 && apt-get install -y build-essential bash \
 && rm -rf /var/lib/apt/lists/*

# Arbeitsverzeichnis für deine App
WORKDIR /app

# Python-Abhängigkeiten installieren
COPY zhijinpower/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Quellcode + run.sh kopieren
COPY zhijinpower/ /app
COPY zhijinpower/run.sh /run.sh

# run.sh ausführbar machen
RUN chmod +x /run.sh

# Jetzt run.sh als Entrypoint benutzen
ENTRYPOINT ["/run.sh"]
