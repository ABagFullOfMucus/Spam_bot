FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    libx11-6 \
    libxcb1 \
    libgtk-3-0 \
    libcairo2 \
    libasound2 \
    libfreetype6 \
    libfontconfig1 \
    libdbus-1-3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    playwright install chromium && \
    playwright install-deps chromium

COPY . .

CMD ["python", "main.py"]
