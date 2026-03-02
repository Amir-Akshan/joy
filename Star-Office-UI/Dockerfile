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

# Ensure optional state files exist (create sensible defaults if not provided)
RUN if [ ! -f /app/agent-invite-template.txt ]; then echo "" > /app/agent-invite-template.txt; fi && \
    if [ ! -f /app/agents-state.json ]; then echo '[]' > /app/agents-state.json; fi && \
    if [ ! -f /app/join-keys.json ]; then echo '{"keys": []}' > /app/join-keys.json; fi && \
    if [ ! -f /app/state.json ]; then echo '{}' > /app/state.json; fi && \
    if [ ! -f /app/state.sample.json ]; then echo '{}' > /app/state.sample.json; fi

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
