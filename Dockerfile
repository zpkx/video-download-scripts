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
    mkdir -p /app && \
    chown -R downloader:downloader /app

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY video_downloader.py .

# Copy config files from config folder (if they exist)
COPY config/ ./config/

# Switch to non-root user
USER downloader

# Set default command
ENTRYPOINT ["python3", "/app/video_downloader.py"]
CMD []
