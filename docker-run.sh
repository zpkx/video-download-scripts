#!/bin/bash

# Video Downloader Docker Helper Script
# This script provides easy commands to run the video downloader in Docker

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE_NAME="video-downloader"
CONTAINER_NAME="video-downloader"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Build the Docker image
build() {
    log_info "Building Docker image..."
    docker build -t "$IMAGE_NAME" "$SCRIPT_DIR"
    log_success "Docker image built successfully!"
}

# Run with docker-compose
compose_up() {
    log_info "Starting with docker-compose..."
    docker-compose up
}

# Run one-shot command
run_oneshot() {
    log_info "Running one-shot command: $*"
    docker run --rm \
        -v "$SCRIPT_DIR/downloads:/downloads" \
        -v "$SCRIPT_DIR/config:/app/config" \
        -v "$SCRIPT_DIR:/app/local:ro" \
        "$IMAGE_NAME" "$@"
}

# Run interactive container
run_interactive() {
    log_info "Starting interactive container..."
    docker run --rm -it \
        -v "$SCRIPT_DIR/downloads:/downloads" \
        -v "$SCRIPT_DIR/config:/app/config" \
        -v "$SCRIPT_DIR:/app/local:ro" \
        --entrypoint /bin/bash \
        "$IMAGE_NAME"
}

# Download from URLs file
download_from_file() {
    local file_path="${1:-}"
    
    if [[ -n "$file_path" ]]; then
        # Use explicitly specified file
        log_info "Downloading from file: $file_path"
        if [[ ! -f "$SCRIPT_DIR/$file_path" ]]; then
            log_error "File not found: $file_path"
            exit 1
        fi
        docker run --rm \
            -v "$SCRIPT_DIR/downloads:/downloads" \
            -v "$SCRIPT_DIR/config:/app/config" \
            -v "$SCRIPT_DIR:/app/local:ro" \
            "$IMAGE_NAME" -f "/app/local/$file_path"
    else
        # Auto-detect config files (no -f argument needed)
        log_info "Auto-detecting configuration files..."
        docker run --rm \
            -v "$SCRIPT_DIR/downloads:/downloads" \
            -v "$SCRIPT_DIR/config:/app/config" \
            -v "$SCRIPT_DIR:/app/local:ro" \
            "$IMAGE_NAME"
    fi
}

# Get video info only
info_only() {
    local file_path="${1:-}"
    
    if [[ -n "$file_path" ]]; then
        # Use explicitly specified file
        log_info "Getting video info from file: $file_path"
        if [[ ! -f "$SCRIPT_DIR/$file_path" ]]; then
            log_error "File not found: $file_path"
            exit 1
        fi
        docker run --rm \
            -v "$SCRIPT_DIR/config:/app/config" \
            -v "$SCRIPT_DIR:/app/local:ro" \
            "$IMAGE_NAME" --info-only -f "/app/local/$file_path"
    else
        # Auto-detect config files (no -f argument needed)
        log_info "Auto-detecting configuration files for info extraction..."
        docker run --rm \
            -v "$SCRIPT_DIR/config:/app/config" \
            -v "$SCRIPT_DIR:/app/local:ro" \
            "$IMAGE_NAME" --info-only
    fi
}

# Clean up containers and images
cleanup() {
    log_info "Cleaning up Docker containers and images..."
    
    # Stop and remove container if running
    if docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
        docker stop "$CONTAINER_NAME"
        docker rm "$CONTAINER_NAME"
    fi
    
    # Remove image
    if docker images -q "$IMAGE_NAME" | grep -q .; then
        docker rmi "$IMAGE_NAME"
    fi
    
    log_success "Cleanup completed!"
}

# Show usage
usage() {
    cat << EOF
Video Downloader Docker Helper

Usage: $0 <command> [options]

Commands:
    build                   Build the Docker image
    download [file]         Download videos from file (default: config/urls.yaml)
    info [file]             Get video info only from file (default: config/urls.yaml)
    run <args>              Run one-shot command with arguments
    interactive             Start interactive bash session
    compose                 Start with docker-compose
    cleanup                 Clean up Docker containers and images
    help                    Show this help message

Examples:
    $0 build
    $0 download                      # Uses config/urls.yaml automatically
    $0 download urls.yaml            # Uses specific file from root
    $0 info                          # Gets info from config/urls.yaml automatically
    $0 info urls.yaml                # Gets info from specific file
    $0 run --help
    $0 run --quality high            # Uses config files automatically
    $0 run -f /app/local/urls.yaml --quality high
    $0 interactive
    $0 cleanup

EOF
}

# Main script logic
case "${1:-help}" in
    build)
        build
        ;;
    download)
        download_from_file "$2"
        ;;
    info)
        info_only "$2"
        ;;
    run)
        shift
        run_oneshot "$@"
        ;;
    interactive|shell|bash)
        run_interactive
        ;;
    compose|up)
        compose_up
        ;;
    cleanup|clean)
        cleanup
        ;;
    help|--help|-h)
        usage
        ;;
    *)
        log_error "Unknown command: $1"
        usage
        exit 1
        ;;
esac
