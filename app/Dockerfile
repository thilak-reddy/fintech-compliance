# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install system dependencies (git is needed for change management, openssl for TLS-related tasks)
RUN apt-get update && apt-get install -y \
    git \
    openssl \
 && rm -rf /var/lib/apt/lists/*

# Create a non-root user 'app_user'
RUN useradd -m app_user

# Set working directory to /app
WORKDIR /app

# Copy the entire app directory contents into /app
COPY . /app

# Install required Python packages
RUN pip install --no-cache-dir cryptography

# Ensure all files are owned by app_user
RUN chown -R app_user:app_user /app

# Switch to non-root user (this is important for some controls which check file ownership)
USER app_user

# Expose the HTTPS port (your app uses 8443 – note that tls_check.rb expects 443; you may wish to update that control)
EXPOSE 8443

# Run the application
CMD ["python", "app.py"]
