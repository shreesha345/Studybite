# Use Python base image
FROM python:3.12.4-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy all API directories
COPY api1/ api1/
COPY api2/ api2/
COPY api3/ api3/

# Install supervisor to manage multiple processes and ffmpeg
RUN apt-get update && apt-get install -y \
    supervisor \
    ffmpeg \
    && apt-get clean

# Copy supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose the ports
EXPOSE 8000 8001 8002

# Start supervisor to manage the APIs
CMD ["/usr/bin/supervisord"]
