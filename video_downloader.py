import yt_dlp
import os
import sys
import argparse
import logging
import json
from typing import List, Optional, Dict, Any
import time
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("video_download.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class VideoDownloader:
    """Enhanced video downloader using yt-dlp with improved features"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.default_config = self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration for yt-dlp"""
        return {
            "format": "bestvideo[height>=720]+bestaudio/best[acodec!=none]",
            "merge_output_format": "mp4",
            "writeinfojson": True,
            "writesubtitles": True,
            "writeautomaticsub": True,
            "subtitleslangs": ["zh-CN", "zh-TW", "en"],
            "ignoreerrors": True,
            "no_warnings": False,
            "extractaudio": False,
            "audioformat": "mp3",
            "embed_subs": True,
            "writedesctription": True,
            "writethumbnail": True,
        }

    def _get_cookies_file(self) -> Optional[str]:
        """Find cookies file in common locations"""
        possible_paths = [
            "cookies.txt",
            "www.bilibili.com_cookies.txt",
            os.path.expanduser("~/cookies.txt"),
            os.path.expanduser("~/Downloads/cookies.txt"),
        ]

        for path in possible_paths:
            if os.path.exists(path):
                logger.info(f"Found cookies file: {path}")
                return path

        logger.warning("No cookies file found. Some videos may not be accessible.")
        return None

    def _get_ffmpeg_location(self) -> Optional[str]:
        """Find ffmpeg installation"""
        # Check if ffmpeg is in PATH
        import shutil

        ffmpeg_path = shutil.which("ffmpeg")
        if ffmpeg_path:
            return ffmpeg_path

        # Check common installation paths
        common_paths = [
            "/usr/local/bin/ffmpeg",
            "/opt/homebrew/bin/ffmpeg",  # macOS with Homebrew
            "C:\\ffmpeg\\bin\\ffmpeg.exe",  # Windows
            "D:\\tools\\ffmpeg\\bin\\ffmpeg.exe",  # Windows alternative
        ]

        for path in common_paths:
            if os.path.exists(path):
                return path

        logger.warning("FFmpeg not found. Video processing may be limited.")
        return None

    def _create_output_template(self, output_dir: str) -> str:
        """Create output template with better naming"""
        return os.path.join(output_dir, "%(uploader)s - %(title)s [%(id)s].%(ext)s")

    def download_videos(
        self,
        urls: List[str],
        output_dir: str = "./downloads",
        quality: str = "best",
        delay_range: tuple = (5, 10),
    ) -> Dict[str, List[str]]:
        """
        Download videos from URLs

        Args:
            urls: List of video URLs
            output_dir: Output directory for downloads
            quality: Video quality preference
            delay_range: Range for random delays between downloads

        Returns:
            Dictionary with successful and failed downloads
        """
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        # Prepare yt-dlp options
        ydl_opts = self.default_config.copy()
        ydl_opts.update(self.config)

        # Set output template
        ydl_opts["outtmpl"] = self._create_output_template(output_dir)

        # Set cookies file if available
        cookies_file = self._get_cookies_file()
        if cookies_file:
            ydl_opts["cookiefile"] = cookies_file

        # Set ffmpeg location if available
        ffmpeg_location = self._get_ffmpeg_location()
        if ffmpeg_location:
            ydl_opts["ffmpeg_location"] = os.path.dirname(ffmpeg_location)

        # Adjust quality settings
        if quality == "high":
            ydl_opts["format"] = "bestvideo[height>=1080]+bestaudio/best"
        elif quality == "medium":
            ydl_opts["format"] = "bestvideo[height>=720]+bestaudio/best"
        elif quality == "low":
            ydl_opts["format"] = "worst[height>=480]/worst"

        successful_downloads = []
        failed_downloads = []

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for i, url in enumerate(urls, 1):
                try:
                    logger.info(f"Downloading video {i}/{len(urls)}: {url}")
                    ydl.download([url])
                    successful_downloads.append(url)
                    logger.info(f"Successfully downloaded: {url}")

                    # Add delay between downloads to avoid rate limiting
                    if i < len(urls):
                        delay = random.randint(*delay_range)
                        logger.info(f"Waiting {delay} seconds before next download...")
                        time.sleep(delay)

                except Exception as e:
                    logger.error(f"Error downloading {url}: {e}")
                    failed_downloads.append(url)

        return {"successful": successful_downloads, "failed": failed_downloads}

    def get_video_info(self, url: str) -> Optional[Dict[str, Any]]:
        """Get video information without downloading"""
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
        }

        cookies_file = self._get_cookies_file()
        if cookies_file:
            ydl_opts["cookiefile"] = cookies_file

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
        except Exception as e:
            logger.error(f"Error extracting info for {url}: {e}")
            return None


def load_urls_from_file(file_path: str) -> List[str]:
    """Load URLs from a text file"""
    urls = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    urls.append(line)
        logger.info(f"Loaded {len(urls)} URLs from {file_path}")
    except Exception as e:
        logger.error(f"Error loading URLs from file: {e}")

    return urls


def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(
        description="Enhanced video downloader using yt-dlp"
    )
    parser.add_argument("urls", nargs="*", help="Video URLs to download")
    parser.add_argument("-f", "--file", help="File containing URLs (one per line)")
    parser.add_argument(
        "-o", "--output", default="./downloads", help="Output directory"
    )
    parser.add_argument(
        "-q",
        "--quality",
        choices=["low", "medium", "high", "best"],
        default="best",
        help="Video quality",
    )
    parser.add_argument(
        "--delay-min",
        type=int,
        default=5,
        help="Minimum delay between downloads (seconds)",
    )
    parser.add_argument(
        "--delay-max",
        type=int,
        default=10,
        help="Maximum delay between downloads (seconds)",
    )
    parser.add_argument(
        "--info-only", action="store_true", help="Extract video info only (no download)"
    )
    parser.add_argument("--config", help="JSON config file for yt-dlp options")

    args = parser.parse_args()

    # Load configuration if provided
    config = {}
    if args.config and os.path.exists(args.config):
        try:
            with open(args.config, "r") as f:
                config = json.load(f)
        except Exception as e:
            logger.error(f"Error loading config file: {e}")

    # Get URLs
    urls = args.urls or []
    if args.file:
        urls.extend(load_urls_from_file(args.file))

    if not urls:
        logger.error("No URLs provided. Use --help for usage information.")
        return

    # Initialize downloader
    downloader = VideoDownloader(config)

    if args.info_only:
        # Just extract info
        for url in urls:
            info = downloader.get_video_info(url)
            if info:
                print(f"\nTitle: {info.get('title', 'N/A')}")
                print(f"Uploader: {info.get('uploader', 'N/A')}")
                print(f"Duration: {info.get('duration', 'N/A')} seconds")
                print(f"View count: {info.get('view_count', 'N/A')}")
                print(f"URL: {url}")
                print("-" * 50)
    else:
        # Download videos
        result = downloader.download_videos(
            urls, args.output, args.quality, (args.delay_min, args.delay_max)
        )

        # Print summary
        print(f"\n{'='*50}")
        print("Download Summary:")
        print(f"Successful: {len(result['successful'])}")
        print(f"Failed: {len(result['failed'])}")

        if result["failed"]:
            print("\nFailed downloads:")
            for url in result["failed"]:
                print(f"  - {url}")


if __name__ == "__main__":
    # Example usage when run directly
    if len(sys.argv) == 1:
        # Default example for testing
        video_urls = ["https://www.bilibili.com/video/av114543489451440?t=1.2"]
        output_dir = "./downloads"

        downloader = VideoDownloader()
        result = downloader.download_videos(video_urls, output_dir)

        print("Download completed:")
        print(f"Successful: {len(result['successful'])}")
        print(f"Failed: {len(result['failed'])}")
    else:
        main()
