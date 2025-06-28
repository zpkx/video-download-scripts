# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m -u 1000 downloader && \
    mkdir -p /app /downloads /config && \
    chown -R downloader:downloader /app /downloads /config

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY video_downloader.py .

# Copy config files from config folder (if they exist)
COPY config/ ./config/
# Also copy any root-level config files for backward compatibility
COPY config.yaml* ./
COPY urls.yaml* ./
COPY cookies.txt* ./

# Make video_downloader.py executable
RUN chmod +x video_downloader.py

# Switch to non-root user
USER downloader

# Create volumes for persistent data
VOLUME ["/downloads", "/config"]

# Set default command
ENTRYPOINT ["python3", "/app/video_downloader.py"]
CMD []
