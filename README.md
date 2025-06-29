# Video Downloader

A powerful and flexible video downloader built with yt-dlp, featuring YAML-based configuration, categorized downloads, and automatic configuration detection.

## ✨ Features

- **YAML Configuration**: Easily edit both URL lists and yt-dlp options using YAML files
- **Auto-Configuration**: Automatically detects and loads `config.yaml` and `urls.yaml` if present
- **File Monitoring**: Automatically starts downloads when `urls.yaml` is modified (Docker mode)
- **Categorized Downloads**: Organize downloads by category, each with its own output directory and settings
- **Flexible Input**: Support for both YAML config files and command-line URLs
- **Info-Only Mode**: Extract video metadata without downloading
- **Dry-Run Mode**: Preview downloads without saving files
- **Docker Support**: Containerized deployment with helper scripts and Docker Compose
- **Delay Management**: Configurable random delays between downloads to avoid rate limiting
- **Cookie Support**: Automatically detects cookie files for authenticated downloads
- **Comprehensive Logging**: Detailed logs for monitoring progress, errors, and configuration loading

## 🚀 Quick Start

### Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Docker Installation (Alternative)

For containerized deployment, you can use Docker:

1. **设置用户权限** (推荐):
   ```bash
   # 自动设置当前用户的 UID/GID
   ./setup-env.sh
   
   # 或者手动创建 .env 文件
   echo "USER_UID=$(id -u)" > .env
   echo "USER_GID=$(id -g)" >> .env
   ```

2. Build the Docker image:
   ```bash
   ./docker-run.sh build
   ```

3. Run with Docker:
   ```bash
   # Download from config/urls.yaml (auto-detected)
   ./docker-run.sh download
   
   # Download from specific file
   ./docker-run.sh download my-urls.yaml
   
   # Get video info only
   ./docker-run.sh info
   ```

#### 环境变量配置

为了避免文件权限问题，项目支持通过环境变量设置 UID/GID：

```bash
# 方法 1: 使用脚本自动设置
./setup-env.sh

# 方法 2: 手动设置环境变量
export USER_UID=$(id -u)
export USER_GID=$(id -g)
docker-compose up -d video-download-watcher

# 方法 3: 在 .env 文件中设置
cp .env.example .env
# 编辑 .env 文件设置你的 UID/GID
```

### Basic Usage

```bash
# Download single video
python video_downloader.py "https://example.com/video"

# Download from YAML config file
python video_downloader.py --file urls.yaml

# Get video info only (no download)
python video_downloader.py --info-only "https://example.com/video"

# Preview what would be downloaded (dry run)
python video_downloader.py --dry-run "https://example.com/video"
```

#### Docker Usage
```bash
# Start file monitoring service (automatically downloads when urls.yaml changes)
./start-watcher.sh

# Alternative: Use Docker Compose directly
docker-compose up video-download-watcher

# Download using Docker (auto-detects config files)
./docker-run.sh download

# Get video info with Docker
./docker-run.sh info

# Manual one-time download
docker-compose run --rm video-downloader-oneshot -f /app/config/urls.yaml

# Custom Docker command
./docker-run.sh run --dry-run "https://example.com/video"
```

#### File Monitoring Feature
The Docker setup includes a file monitoring service that automatically starts downloads when `config/urls.yaml` is modified:

1. **Start the monitoring service**: `./start-watcher.sh`
2. **Edit your URLs**: Modify `config/urls.yaml` to add/remove video URLs
3. **Automatic download**: The service detects changes and starts downloading immediately
4. **View logs**: Monitor the download progress in the terminal

This is perfect for automated setups where you want to add URLs to a file and have them downloaded automatically.

## 📁 Configuration

### Auto-Configuration

The script automatically looks for `config.yaml` or `config.yml` in the `config/` directory and loads yt-dlp options from it. No need to specify the config file manually!

### YAML Configuration Format

#### URLs Configuration (`urls.yaml`)

```yaml
# Global settings applied to all categories
global_settings:
  default_quality: "best"
  default_delay_range: [5, 10]
  default_output_path: "./downloads"

# Category definitions
categories:
  documentaries:
    output_path: "./downloads/documentaries"
    quality: "1080p"
    urls:
      - https://example.com/doc1
      - https://example.com/doc2
  
  tutorials:
    output_path: "./downloads/tutorials"
    urls:
      - https://example.com/tutorial1
      - https://example.com/tutorial2
```

#### yt-dlp Options (`config.yaml`)

```yaml
# Video format and quality
format: "bestvideo[height>=1080]+bestaudio/best"
merge_output_format: "mp4"

# Metadata and subtitles
writeinfojson: true
writesubtitles: true
writeautomaticsub: true
subtitleslangs: ["en", "zh-CN"]
embed_subs: true
writethumbnail: true

# Error handling
ignoreerrors: true
retries: 3
fragment_retries: 3

# Cookie file (optional) - can be specified directly or in global_settings
# cookiefile: "path/to/your/cookies.txt"

# Alternative: specify in global_settings section
# global_settings:
#   cookies_file: "config/cookies.txt"
```

## 📖 Command Line Options
### Command Line Arguments

The script supports the following command line arguments:

| Argument                  | Description                                                      | Default                |
|---------------------------|------------------------------------------------------------------|------------------------|
| `urls`                    | One or more video URLs to download                               |                        |
| `-h`, `--help`            | Show help message and exit                                       |                        |
| `-f FILE`, `--file FILE`  | YAML file with categorized URLs and settings                     |                        |
| `-o OUTPUT`, `--output OUTPUT` | Output directory for downloads                           | `./downloads`          |
| `-q {low,medium,high,best}`, `--quality {low,medium,high,best}` | Video quality         | `best`                 |
| `--delay-min DELAY_MIN`   | Minimum delay (seconds) between downloads                        | `5`                    |
| `--delay-max DELAY_MAX`   | Maximum delay (seconds) between downloads                        | `15`                   |
| `--info-only`             | Extract video info only (no download)                            |                        |
| `--dry-run`               | Show what would be downloaded without downloading                |                        |
| `--config CONFIG`         | YAML config file for yt-dlp options (auto-detects `config.yaml`) |                        |

**Notes:**
- If both URLs and `--file` are specified, only the file is processed.
- If neither URLs nor `--file` are specified, the script auto-detects `config/urls.yaml` if present.
- Use `--info-only` or `--dry-run` for non-destructive operations.

## 🎯 Usage Examples

### Categorized Downloads

Create a `urls.yaml` file:
```yaml
categories:
  anime:
    output_path: "./downloads/anime"
    urls:
      - https://example.com/anime1
      - https://example.com/anime2
  
  movies:
    output_path: "./downloads/movies"
    quality: "best"
    urls:
      - https://example.com/movie1
```

Run the downloader:
```bash
python video_downloader.py --file urls.yaml
```

### Custom yt-dlp Configuration

Create a `config.yaml` file with your preferred yt-dlp options:
```yaml
format: "bestvideo[height<=720]+bestaudio/best"
writesubtitles: true
subtitleslangs: ["en"]
```

The script will automatically load this configuration!

### Info-Only Mode

Extract metadata without downloading:
```bash
python video_downloader.py --info-only "https://example.com/video"
```

### Dry-Run Mode

Preview what would be downloaded without actually downloading:
```bash
# See what would be downloaded
python video_downloader.py --dry-run "https://example.com/video"

# Preview categorized downloads
python video_downloader.py --dry-run --file urls.yaml
```

### Multiple URLs

```bash
python video_downloader.py "url1" "url2" "url3" --output ./my_downloads
```

## 🗂️ File Structure

```
video-downloader/
├── video_downloader.py     # Main script
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Docker Compose configuration
├── docker-run.sh          # Docker helper script
├── .dockerignore          # Docker build exclusions
├── config/                # Configuration directory
│   ├── config.yaml        # yt-dlp options (auto-loaded)
│   ├── urls.yaml          # Categorized URLs configuration
│   └── cookies.txt        # Browser cookies (optional)
├── downloads/             # Default download directory
└── video_download.log     # Download logs
```

## 🔧 Configuration Files

### Supported Cookie Files
The script automatically detects cookies from these locations in order:
1. Path specified in `config.yaml` under `cookiefile` setting
2. Path specified in `config.yaml` under `global_settings.cookies_file` 
3. `config/cookies.txt` (default location)

If no cookies file is found, some authenticated content may not be accessible.

## 📋 Quality Options

- **low**: Lower quality, smaller file size
- **medium**: Balanced quality and size
- **high**: High quality
- **best**: Best available quality (default)

## 🛠️ Advanced Features

### Dry-Run Testing
Preview downloads without using bandwidth or storage:
```bash
# Test single URL
python video_downloader.py --dry-run "https://example.com/video"

# Test categorized downloads
python video_downloader.py --dry-run --file urls.yaml

# Test with custom quality settings
python video_downloader.py --dry-run --quality medium "https://example.com/video"
```

### Delay Configuration
Control download speed to avoid rate limiting:
```bash
# 5-15 second random delays
python video_downloader.py --delay-min 5 --delay-max 15 --file urls.yaml
```

### Custom Output Directories
```bash
python video_downloader.py --output ./custom_folder "https://example.com/video"
```

### Multiple Configuration Files
```bash
# Use specific config file
python video_downloader.py --config my_config.yaml --file urls.yaml
```

## 🐳 Docker Usage

### Docker Helper Script

The included `docker-run.sh` script provides convenient Docker operations:

```bash
# Build the Docker image
./docker-run.sh build

# Download videos (auto-detects config files)
./docker-run.sh download
./docker-run.sh download my-urls.yaml

# Get video information only
./docker-run.sh info
./docker-run.sh info urls.yaml

# Run custom commands
./docker-run.sh run --dry-run "https://example.com/video"
./docker-run.sh run --quality high --file urls.yaml

# Interactive shell for debugging
./docker-run.sh interactive

# Start with docker-compose
./docker-run.sh compose

# Cleanup containers and images
./docker-run.sh cleanup
```

### Manual Docker Commands

If you prefer using Docker directly:

```bash
# Build image
docker build -t video-downloader .

# Run with local files
docker run --rm \
  -v "$(pwd)/downloads:/downloads" \
  -v "$(pwd)/config:/app/config" \
  -v "$(pwd):/app/local:ro" \
  video-downloader

# Run with specific options
docker run --rm \
  -v "$(pwd)/downloads:/downloads" \
  -v "$(pwd)/config:/app/config" \
  video-downloader --dry-run --quality high
```

### Docker Compose

```bash
# Start the service
docker-compose up

# Run one-shot download
docker-compose run --rm video-downloader-oneshot

# Run with specific file
docker-compose run --rm video-downloader-oneshot -f /app/local/urls.yaml
```

### Docker Volume Mounts

- `/downloads` - Where downloaded videos are saved
- `/app/config` - Config folder (urls.yaml, config.yaml, cookies.txt)
- `/app/local` - Read-only access to local files

### Docker Benefits

- **Isolated Environment**: No need to install Python dependencies locally
- **Consistent Behavior**: Same environment across different systems
- **Security**: Runs as non-root user with limited permissions
- **Easy Cleanup**: Remove containers without affecting your system

## 📝 Logging

All download activities are logged to `video_download.log` with timestamps and detailed information about:
- Download progress
- Errors and warnings
- Configuration loading
- File detection

## 🚨 Troubleshooting

### Common Issues

1. **No videos downloaded**: Ensure that `cookies.txt` is present in the `config/` directory if downloading from sites that require authentication. Also, verify that your URLs are correct and accessible.
2. **Configuration not loaded**: Make sure `config.yaml` is located in the `config/` directory, as the script auto-loads configuration from `config/config.yaml` or `config/config.yml`
3. **Network errors**: Increase delay between downloads with `--delay-min` and `--delay-max`
4. **Configuration errors**: Check for correct YAML syntax and option names
5. **URLs ignored when using file**: When both `--file` and URLs are specified, only the file is processed

### Auto-Detection Behavior

- **With URLs specified**: `config/urls.yaml` is not auto-detected, only specified URLs are processed
- **Without URLs**: `config/urls.yaml` is auto-detected if present
- **With --file specified**: The specified file takes priority over any URLs or auto-detection

### Configuration Validation

To verify your configuration is working correctly:
```bash
# Use dry-run to test configuration without downloading
python video_downloader.py --dry-run "https://example.com/test-video"

# Check if config.yaml is being loaded (should show "Loaded X configuration options")
python video_downloader.py --info-only "https://example.com/test-video"
```

### Docker-Specific Issues

1. **Permission Issues**: If you have permission issues with downloads:
   ```bash
   sudo chown -R 1000:1000 downloads/
   ```

2. **Container Updates**: To update after code changes:
   ```bash
   ./docker-run.sh cleanup
   ./docker-run.sh build
   ```

3. **Debug Container**: For troubleshooting:
   ```bash
   ./docker-run.sh interactive
   ```

### Debug Mode

For detailed debugging, check the `video_download.log` file or run with verbose output.

## 📄 License

This project is open source. Use responsibly and respect content creators' rights and platform terms of service.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool.
