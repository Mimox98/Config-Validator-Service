# Multi-stage Dockerfile for Config Validator Service

FROM python:3.11-slim as base

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY configs/ ./configs/

# Expose port for FastAPI
EXPOSE 8000

# Default command: run FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
