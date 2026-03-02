FROM python:3.9-slim
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY landing.html ./
COPY docs/ ./docs/

# (Optional) copy common repo files used by the app
COPY agent-invite-template.txt ./
COPY agents-state.json ./
COPY join-keys.json ./
COPY state.json ./
COPY state.sample.json ./

# Set environment variable
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 18791

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:18791/health || exit 1

# Run the application
CMD ["python", "backend/app.py"]
