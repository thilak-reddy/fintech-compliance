FROM python:3.11-slim

# Create non-root user
RUN useradd -m -s /bin/bash app_user

WORKDIR /app

# Copy only the files that exist
COPY app.py .
COPY config/password_policy.json ./config/

# Create directories if you need them
RUN mkdir -p config docs backup

# If you have specific files that must go in these directories,
# copy them individually or create placeholder files
# For example:
# COPY config/*.json ./config/ || true
# COPY docs/*.md ./docs/ || true
# COPY backup/*.* ./backup/ || true

# Create required directories
RUN mkdir -p logs logs/incidents && \
    chown -R app_user:app_user /app && \
    chmod 644 app.py && \
    chmod 600 config/password_policy.json && \
    chmod 755 logs && \
    chmod 750 logs/incidents && \
    chmod 755 backup

# Switch to non-root user
USER app_user

CMD ["python", "app.py"]
