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
    inotify-tools \
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
# Also copy any root-level config files for backward compatibility
COPY config.yaml* ./
COPY urls.yaml* ./
COPY cookies.txt* ./

# Make video_downloader.py executable
RUN chmod +x video_downloader.py

# Create file watcher script
RUN echo '#!/bin/bash\n\
echo "Starting file watcher for /app/config/urls.yaml..."\n\
\n\
# Function to run download\n\
run_download() {\n\
    echo "$(date): urls.yaml changed, starting download..."\n\
    python3 /app/video_downloader.py -f /app/config/urls.yaml\n\
    echo "$(date): Download completed"\n\
}\n\
\n\
# Run initial download\n\
run_download\n\
\n\
# Watch for file changes\n\
while true; do\n\
    inotifywait -e modify,move,create /app/config/urls.yaml 2>/dev/null\n\
    if [ $? -eq 0 ]; then\n\
        # Add a small delay to ensure file write is complete\n\
        sleep 2\n\
        run_download\n\
    fi\n\
done' > /app/watch-and-download.sh && \
    chmod +x /app/watch-and-download.sh

# Switch to non-root user
USER downloader

# Set default command
ENTRYPOINT ["python3", "/app/video_downloader.py"]
CMD []
