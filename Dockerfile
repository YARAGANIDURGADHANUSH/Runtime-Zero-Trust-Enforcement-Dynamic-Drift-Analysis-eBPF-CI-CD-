# Stage 1: Build stage
FROM python:3.11-slim AS builder

WORKDIR /app

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt


# Stage 2: Runtime stage
FROM python:3.11-slim AS runner

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/home/appuser/.local/bin:$PATH

# Create a non-root system user and group for Principle of Least Privilege
RUN addgroup --system appuser && adduser --system --group appuser

# Copy installed dependencies from builder stage
COPY --from=builder /root/.local /home/appuser/.local
COPY app/ .

# Assign ownership to non-root user
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

# Health check to ensure container status monitoring
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

CMD ["python", "main.py"]