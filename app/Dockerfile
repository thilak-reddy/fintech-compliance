FROM python:3.9-slim

# Install required system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openssl \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r app_user && useradd -r -g app_user app_user

# Set up application directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create required directories with proper permissions
RUN mkdir -p backup logs/incidents docs config && \
    chown -R app_user:app_user /app && \
    chmod 755 logs && \
    chmod 750 logs/incidents && \
    chmod 755 config && \
    chmod 600 config/password_policy.json

# Switch to non-root user
USER app_user

# Expose the port used in app.py (8443)
EXPOSE 8443

# Health check using the correct port
HEALTHCHECK --interval=30s --timeout=5s \
    CMD curl -k https://localhost:8443/health || exit 1

# Run the application
CMD ["python3", "app.py"]