# Dockerfile for Prism Alerts
# Build: docker build -t prism-alerts .
# Run: docker run -e PRISM_URL=https://... prism-alerts

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY alerts.py .
COPY entrypoint.py .
COPY .env.example .env

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('https://strykr-prism.up.railway.app/crypto/trending/solana/bonding')" || exit 1

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV COMMAND=watch

# Run
ENTRYPOINT ["python", "entrypoint.py"]
CMD ["watch"]
