# Video Downloader Docker Setup

This directory contains Docker configuration files to run the video downloader in a containerized environment.

## Files

- `Dockerfile` - Docker image definition
- `docker-compose.yml` - Docker Compose configuration
- `docker-run.sh` - Helper script for common Docker operations
- `.dockerignore` - Files to exclude from Docker build context

## Quick Start

### 1. Build the Docker image
```bash
./docker-run.sh build
```

### 2. Download videos from your URLs file
```bash
# Download from config/urls.yaml (auto-detected)
./docker-run.sh download

# Download from a specific file
./docker-run.sh download my-urls.yaml
```

### 3. Get video information only (no download)
```bash
# Get info from config/urls.yaml (auto-detected)
./docker-run.sh info

# Get info from specific file
./docker-run.sh info urls.yaml
```

## Usage Options

### Using the helper script (Recommended)
```bash
# Build image
./docker-run.sh build

# Download videos
./docker-run.sh download                  # Uses config/urls.yaml automatically
./docker-run.sh download urls.yaml        # Uses specific file

# Get video info only
./docker-run.sh info                      # Uses config/urls.yaml automatically
./docker-run.sh info urls.yaml            # Uses specific file

# Run custom command
./docker-run.sh run --help
./docker-run.sh run -f /app/local/urls.yaml --quality high

# Interactive shell
./docker-run.sh interactive

# Start with docker-compose
./docker-run.sh compose

# Cleanup
./docker-run.sh cleanup
```

### Using Docker directly
```bash
# Build image
docker build -t video-downloader .

# Run with local files
docker run --rm \
  -v "$(pwd)/downloads:/downloads" \
  -v "$(pwd)/config:/app/config" \
  -v "$(pwd):/app/local:ro" \
  video-downloader

# Run with specific file
docker run --rm \
  -v "$(pwd)/downloads:/downloads" \
  -v "$(pwd)/config:/app/config" \
  -v "$(pwd):/app/local:ro" \
  video-downloader -f /app/local/urls.yaml

# Get video info only
docker run --rm \
  -v "$(pwd)/config:/app/config" \
  -v "$(pwd):/app/local:ro" \
  video-downloader --info-only
```

### Using Docker Compose
```bash
# Start the service (will show help by default)
docker-compose up

# Run one-shot download (auto-detects config/urls.yaml)
docker-compose run --rm video-downloader-oneshot

# Run with specific file
docker-compose run --rm video-downloader-oneshot -f /app/local/urls.yaml

# Override command in docker-compose.yml
# Edit the 'command' section to specify your desired arguments
```

## Volume Mounts

- `/downloads` - Where downloaded videos are saved
- `/app/config` - Config folder containing urls.yaml, config.yaml, cookies.txt
- `/app/local` - Read-only access to your local files (for backward compatibility)
- `/config` - Legacy mount point (still supported)

## Environment Setup

The Docker container includes:
- Python 3.12
- yt-dlp and dependencies
- FFmpeg for video processing
- Non-root user for security

## Configuration Files

The Docker setup now supports the improved config folder structure:
- `config/urls.yaml` - Your video URLs and categories (auto-detected)
- `config/config.yaml` - yt-dlp configuration options (auto-detected)
- `config/cookies.txt` - Browser cookies for authenticated sites (auto-detected)

For backward compatibility, files in the root directory are still supported:
- `urls.yaml` - Legacy URLs file
- `config.yaml` - Legacy config file
- `cookies.txt` - Legacy cookies file

## Examples

### Download specific URLs
```bash
./docker-run.sh run "https://example.com/video1" "https://example.com/video2"
```

### Download with auto-detected config
```bash
# Uses config/urls.yaml, config/config.yaml, and config/cookies.txt automatically
./docker-run.sh run
```

### Download with high quality
```bash
# Uses config files automatically
./docker-run.sh run --quality high
```

### Download to specific directory
```bash
# Uses config files automatically
./docker-run.sh run -o /downloads/my-folder
```

### Get help
```bash
./docker-run.sh run --help
```

## Troubleshooting

### Permission Issues
The container runs as user ID 1000. If you have permission issues with the downloads directory:
```bash
sudo chown -R 1000:1000 downloads/
```

### Container Updates
To update the container with code changes:
```bash
./docker-run.sh cleanup
./docker-run.sh build
```

### Debug Container
To troubleshoot issues:
```bash
./docker-run.sh interactive
```

## Security Notes

- The container runs as a non-root user
- Local files are mounted read-only
- Only the downloads directory has write access
- No network ports are exposed by default
