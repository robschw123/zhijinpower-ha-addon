FROM python:3.12-slim

# optionaler Fallback
ENV TZ=Europe/Berlin

# System-Tools  
RUN apt-get update \
 && apt-get install -y build-essential bash \
 && rm -rf /var/lib/apt/lists/*

# Arbeitsverzeichnis  
WORKDIR /app

# Python-Abhängigkeiten installieren  
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Quellcode + run.sh kopieren  
COPY . /app
RUN chmod +x /app/run.sh

# Entrypoint auf dein Bash-Starter-Script  
ENTRYPOINT ["/app/run.sh"]
