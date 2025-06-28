# Video Downloader

A powerful and flexible video downloader built with yt-dlp, featuring YAML-based configuration, categorized downloads, and automatic configuration detection.

## ✨ Features

- **YAML Configuration**: Easy-to-edit configuration files for both URLs and yt-dlp options
- **Auto-Configuration**: Automatically detects and loads `config.yaml` if present
- **Categorized Downloads**: Organize downloads into categories with separate output directories
- **Flexible Input**: Support for both YAML config files and plain text URL lists
- **Info-Only Mode**: Extract video metadata without downloading
- **Delay Management**: Configurable delays between downloads to avoid rate limiting
- **Cookie Support**: Automatic detection of cookie files for authenticated content
- **Comprehensive Logging**: Detailed logs for monitoring download progress

## 🚀 Quick Start

### Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Basic Usage

```bash
# Download single video
python video_downloader.py "https://example.com/video"

# Download from YAML config file
python video_downloader.py --file urls.yaml

# Download from plain text file
python video_downloader.py --file urls.txt

# Get video info only (no download)
python video_downloader.py --info-only "https://example.com/video"
```

## 📁 Configuration

### Auto-Configuration

The script automatically looks for `config.yaml` or `config.yml` in the current directory and loads yt-dlp options from it. No need to specify the config file manually!

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
```

## 📖 Command Line Options

```
usage: video_downloader.py [-h] [-f FILE] [-o OUTPUT] 
                          [-q {low,medium,high,best}] [--delay-seconds DELAY_SECONDS]
                          [--delay-max DELAY_MAX] [--info-only] [--config CONFIG]
                          [urls ...]

positional arguments:
  urls                  Video URLs to download

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  YAML config file or plain text URLs file
  -o OUTPUT, --output OUTPUT
                        Output directory (default: ./downloads)
  -q {low,medium,high,best}, --quality {low,medium,high,best}
                        Video quality (default: best)
  --delay-seconds DELAY_SECONDS
                        Minimum delay between downloads in seconds (default: 5)
  --delay-max DELAY_MAX
                        Maximum delay between downloads in seconds (default: 15)
  --info-only           Extract video info only (no download)
  --config CONFIG       YAML config file for yt-dlp options (auto-detects config.yaml)
```

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

### Multiple URLs

```bash
python video_downloader.py "url1" "url2" "url3" --output ./my_downloads
```

## 🗂️ File Structure

```
video-download-scripts/
├── video_downloader.py     # Main script
├── requirements.txt        # Python dependencies
├── config.yaml            # yt-dlp options (auto-loaded)
├── urls.yaml              # Categorized URLs configuration
├── cookies.txt            # Browser cookies (optional)
├── downloads/             # Default download directory
└── video_download.log     # Download logs
```

## 🔧 Configuration Files

### Supported Cookie Files
The script automatically detects cookies from these locations:
- `cookies.txt`
- `www.bilibili.com_cookies.txt`
- `~/cookies.txt`
- `~/Downloads/cookies.txt`

### Legacy Support
- Plain text URL files (`.txt`) are still supported
- Existing workflows will continue to work

## 📋 Quality Options

- **low**: Lower quality, smaller file size
- **medium**: Balanced quality and size
- **high**: High quality
- **best**: Best available quality (default)

## 🛠️ Advanced Features

### Delay Configuration
Control download speed to avoid rate limiting:
```bash
# 5-15 second random delays
python video_downloader.py --delay-seconds 5 --delay-max 15 --file urls.yaml
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

## 📝 Logging

All download activities are logged to `video_download.log` with timestamps and detailed information about:
- Download progress
- Errors and warnings
- Configuration loading
- File detection

## 🔄 Migration from JSON/TOML

If you have existing JSON or TOML configuration files, refer to the migration guides:
- `JSON_TO_YAML_MIGRATION.md` - Step-by-step migration guide
- `YAML_GUIDE.md` - Complete YAML configuration reference

## 🚨 Troubleshooting

### Common Issues

1. **No videos downloaded**: Check if cookies.txt is present for authenticated content
2. **Configuration not loaded**: Ensure `config.yaml` is in the same directory as the script
3. **Network errors**: Increase delay between downloads with `--delay-seconds`

### Debug Mode

For detailed debugging, check the `video_download.log` file or run with verbose output.

## 📄 License

This project is open source. Use responsibly and respect content creators' rights and platform terms of service.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool.
