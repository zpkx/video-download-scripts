# Video Download Scripts

This repository contains optimized video downloading scripts using `yt-dlp`.

## Features

### Enhanced yt-dlp Script (`video_downloader.py`)

- **Cross-platform compatibility**: Works on Windows, macOS, and Linux
- **Automatic dependency detection**: Finds ffmpeg and cookies automatically
- **Command-line interface**: Full CLI with multiple options
- **Batch downloading**: Support for URL lists from files
- **Quality selection**: Choose video quality (low/medium/high/best)
- **Smart output naming**: Organized file naming with uploader and title
- **Comprehensive logging**: Detailed logs with timestamps
- **Error handling**: Robust error handling with retry logic
- **Rate limiting**: Configurable delays between downloads
- **Configuration support**: JSON config files for advanced options
- **Subtitle support**: Automatic subtitle downloading and embedding
- **Metadata preservation**: Keeps video info, thumbnails, and descriptions

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install ffmpeg (optional but recommended):
   - **macOS**: `brew install ffmpeg`
   - **Ubuntu/Debian**: `sudo apt install ffmpeg`
   - **Windows**: Download from https://ffmpeg.org/download.html

## Usage

### Basic Usage

```bash
# Download a single video
python video_downloader.py "https://www.bilibili.com/video/BV1xx411c7mD"

# Download multiple videos
python video_downloader.py "url1" "url2" "url3"

# Download from URL list file
python video_downloader.py -f urls.txt

# Specify output directory and quality
python video_downloader.py -o ./downloads -q high "url"

# Get video info only (no download)
python video_downloader.py --info-only "url"

# Use custom configuration
python video_downloader.py --config config.json -f urls.txt
```

### Advanced Options

```bash
# Custom delay between downloads (avoid rate limiting)
python video_downloader.py --delay-min 10 --delay-max 20 -f urls.txt

# Different quality options
python video_downloader.py -q low     # 480p or lower
python video_downloader.py -q medium  # 720p
python video_downloader.py -q high    # 1080p
python video_downloader.py -q best    # Best available quality
```

## Configuration

### Cookies (for private/member content)

Place your cookies file in one of these locations:
- `cookies.txt` (same directory)
- `www.bilibili.com_cookies.txt` (same directory)
- `~/cookies.txt` (home directory)
- `~/Downloads/cookies.txt`

### Custom Configuration

Create a `config.json` file with custom yt-dlp options:

```json
{
  "format": "bestvideo[height>=1080]+bestaudio/best",
  "writesubtitles": true,
  "writeautomaticsub": true,
  "subtitleslangs": ["zh-CN", "en"],
  "embed_subs": true
}
```

## File Structure

```
video-download-scripts/
├── video_downloader.py     # Enhanced yt-dlp downloader
├── requirements.txt       # Python dependencies
├── config.json           # Example configuration
├── urls.txt              # Example URL list
└── README.md             # This file
```

## Troubleshooting

### Common Issues

1. **FFmpeg not found**: Install ffmpeg or ensure it's in your PATH
2. **Permission denied**: Check output directory permissions
3. **Network errors**: Use VPN if content is geo-blocked
4. **Rate limiting**: Increase delay between downloads

### Logs

The script creates detailed logs in `video_download.log` for debugging.

## Examples

### Download Bilibili playlist with high quality
```bash
python video_downloader.py -o "./downloads/anime" -q high --delay-min 15 --delay-max 25 "playlist_url"
```

### Batch download with custom config
```bash
python video_downloader.py --config config.json -f urls.txt -o "./downloads"
```

### Extract video information only
```bash
python video_downloader.py --info-only "https://www.bilibili.com/video/BV1xx411c7mD"
```

## Notes

- The script automatically creates output directories
- Downloads include subtitles, thumbnails, and metadata when available
- Failed downloads are logged and reported in the summary
- Cross-platform path handling ensures compatibility across operating systems
