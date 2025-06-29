import yt_dlp
import os
import sys
import argparse
import logging
import json
from typing import List, Optional, Dict, Any
import time
import random
import yaml

# Configure logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "video_download.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class VideoDownloader:
    """Simplified video downloader using yt-dlp with config-based setup"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.default_config = self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration for yt-dlp"""
        return {
            "format": "bestvideo[height>=720]+bestaudio/best[acodec!=none]",
            "merge_output_format": "mp4",
            "writeinfojson": False,
            "writesubtitles": True,
            "writeautomaticsub": True,
            "subtitleslangs": ["zh-CN", "zh-TW", "en"],
            "ignoreerrors": True,
            "no_warnings": False,
            "extractaudio": False,
            "audioformat": "mp3",
            "embed_subs": True,
            "writedescription": True,
            "writethumbnail": True,
        }

    def _get_cookies_file(self) -> Optional[str]:
        """Get cookies file from config directory"""
        # First try to get from user config
        if "cookiefile" in self.config:
            cookies_path = self.config["cookiefile"]
            if os.path.exists(cookies_path):
                logger.info(f"Found cookies file from config: {cookies_path}")
                return cookies_path

        # Fallback to default path
        cookies_path = "config/cookies.txt"
        if os.path.exists(cookies_path):
            logger.info(f"Found cookies file: {cookies_path}")
            return cookies_path

        logger.warning("No cookies file found. Some videos may not be accessible.")
        return None

    def _create_output_template(self, output_dir: str) -> str:
        """Create output template with better naming"""
        return os.path.join(output_dir, "%(title)s.%(ext)s")

    def download_videos(
        self,
        urls: List[str],
        output_dir: str = "./downloads",
        quality: str = "best",
        delay_range: tuple = (5, 10),
        dry_run: bool = False,
    ) -> Dict[str, List[str]]:
        """
        Download videos from URLs

        Args:
            urls: List of video URLs
            output_dir: Output directory for downloads
            quality: Video quality preference
            delay_range: Range for random delays between downloads
            dry_run: If True, only show what would be downloaded without actually downloading

        Returns:
            Dictionary with:
            - successful: List of successfully downloaded URLs
            - failed: List of failed URLs
            - downloaded_files: List of dicts with file info (url, file_path, title)
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

        # Adjust quality settings
        if quality == "high":
            ydl_opts["format"] = "bestvideo[height>=1080]+bestaudio/best"
        elif quality == "medium":
            ydl_opts["format"] = "bestvideo[height>=720]+bestaudio/best"
        elif quality == "low":
            ydl_opts["format"] = "worst[height>=480]/worst"

        successful_downloads = []
        failed_downloads = []
        downloaded_files = []  # Store information about downloaded files

        # Hook function to capture downloaded file paths
        def download_hook(d):
            if d["status"] == "finished":
                file_path = d["filename"]
                downloaded_files.append(
                    {
                        "url": d.get("info_dict", {}).get("webpage_url", "Unknown"),
                        "file_path": os.path.abspath(file_path),
                        "title": d.get("info_dict", {}).get("title", "Unknown"),
                    }
                )
                logger.info(f"Downloaded file: {os.path.abspath(file_path)}")

        # Add the hook to yt-dlp options
        ydl_opts["progress_hooks"] = [download_hook]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for i, url in enumerate(urls, 1):
                try:
                    if dry_run:
                        logger.info(
                            f"[DRY RUN] Would download video {i}/{len(urls)}: {url}"
                        )
                        # Extract info to show what would be downloaded
                        info = ydl.extract_info(url, download=False)
                        if info:
                            title = info.get("title", "Unknown")
                            duration = info.get("duration")
                            if duration is not None:
                                try:
                                    duration_str = (
                                        f"{int(duration)//60}:{int(duration) % 60:02d}"
                                    )
                                except (ValueError, TypeError):
                                    duration_str = "Unknown"
                            else:
                                duration_str = "Unknown"
                            filesize = info.get("filesize") or info.get(
                                "filesize_approx"
                            )
                            filesize_str = (
                                f"{filesize/1024/1024:.1f}MB"
                                if filesize
                                else "Unknown size"
                            )

                            logger.info(f"[DRY RUN] Title: {title}")
                            logger.info(f"[DRY RUN] Duration: {duration_str}")
                            logger.info(f"[DRY RUN] Size: {filesize_str}")
                            logger.info(f"[DRY RUN] Would save to: {output_dir}")

                            # Simulate successful download for dry run
                            downloaded_files.append(
                                {
                                    "url": url,
                                    "file_path": os.path.join(
                                        output_dir, f"{title}.mp4"
                                    ),
                                    "title": title,
                                }
                            )
                        successful_downloads.append(url)
                    else:
                        logger.info(f"Downloading video {i}/{len(urls)}: {url}")
                        ydl.download([url])
                        successful_downloads.append(url)
                        logger.info(f"Successfully downloaded: {url}")

                    # Add delay between downloads to avoid rate limiting
                    if i < len(urls):
                        delay = random.randint(*delay_range)
                        if dry_run:
                            logger.info(
                                f"[DRY RUN] Would wait {delay} seconds before next download..."
                            )
                        else:
                            logger.info(
                                f"Waiting {delay} seconds before next download..."
                            )
                            time.sleep(delay)

                except Exception as e:
                    logger.error(
                        f"Error {'simulating' if dry_run else 'downloading'} {url}: {e}"
                    )
                    failed_downloads.append(url)

        return {
            "successful": successful_downloads,
            "failed": failed_downloads,
            "downloaded_files": downloaded_files,
        }

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


def parse_config_file(file_path: str) -> Dict[str, Any]:
    """
    Parse YAML configuration file

    Args:
        file_path: Path to the YAML configuration file

    Returns:
        Dictionary with yt-dlp configuration options
    """
    config = load_yaml_config(file_path)

    # Extract only yt-dlp specific settings, not our custom categories
    ytdlp_config = {}
    for key, value in config.items():
        if key not in ["categories", "global_settings"]:
            ytdlp_config[key] = value

    # Handle global_settings cookies_file
    global_settings = config.get("global_settings", {})
    if "cookies_file" in global_settings and "cookiefile" not in ytdlp_config:
        ytdlp_config["cookiefile"] = global_settings["cookies_file"]

    return ytdlp_config


def load_yaml_config(file_path: str) -> Dict[str, Any]:
    """Load configuration from YAML file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            return config if config else {}
    except FileNotFoundError:
        logger.error(f"Config file not found: {file_path}")
        return {}
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file: {e}")
        return {}
    except Exception as e:
        logger.error(f"Error loading config file: {e}")
        return {}


def load_categorized_urls(file_path: str) -> Dict[str, Dict[str, Any]]:
    """Load URLs organized by categories from YAML config file"""
    config = load_yaml_config(file_path)

    if not config:
        return {}

    categories = config.get("categories", {})
    global_settings = config.get("global_settings", {})

    # Apply global settings to each category if not specified
    for category_name, category_data in categories.items():
        for setting, default_value in global_settings.items():
            if setting not in category_data and setting != "default_output_path":
                category_data[setting] = default_value

        # Set default output path if not specified
        if "output_path" not in category_data:
            default_output = global_settings.get("default_output_path", "./downloads")
            category_data["output_path"] = os.path.join(default_output, category_name)

    return categories


def download_by_categories(
    downloader: "VideoDownloader",
    categories: Dict[str, Dict[str, Any]],
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Download videos organized by categories"""
    total_results = {"successful": [], "failed": [], "category_results": {}}

    for category_name, category_config in categories.items():
        urls = category_config.get("urls", [])
        if not urls:
            logger.info(f"No URLs found for category: {category_name}")
            continue

        logger.info(f"\n🎯 Processing category: {category_name}")
        logger.info(
            f"📁 Output path: {category_config.get('output_path', './downloads')}"
        )
        logger.info(f"🎬 URLs to download: {len(urls)}")

        # Extract download parameters from category config
        output_dir = category_config.get("output_path", "./downloads")
        quality = category_config.get("quality", "best")
        delay_range = tuple(category_config.get("delay_range", [5, 10]))

        # Update downloader config for this category
        category_downloader_config = {}

        # Handle audio extraction
        if category_config.get("extract_audio", False):
            category_downloader_config["extractaudio"] = True
            category_downloader_config["audioformat"] = category_config.get(
                "audio_format", "mp3"
            )

        # Handle subtitle languages
        if "subtitle_langs" in category_config:
            category_downloader_config["subtitleslangs"] = category_config[
                "subtitle_langs"
            ]

        # Handle thumbnail embedding
        if category_config.get("embed_thumbnail", False):
            category_downloader_config["embedthumbnail"] = True

        # Create a new downloader instance with category-specific config
        temp_downloader = VideoDownloader(category_downloader_config)

        # Download videos for this category
        result = temp_downloader.download_videos(
            urls, output_dir, quality, delay_range, dry_run
        )

        # Store category results
        total_results["category_results"][category_name] = result
        total_results["successful"].extend(result["successful"])
        total_results["failed"].extend(result["failed"])

        # Print category summary
        print(f"\n📊 Category '{category_name}' Summary:")
        print(f"✅ Successful: {len(result['successful'])}")
        if len(result["failed"]) > 0:
            print(f"❌ Failed: {len(result['failed'])}")

        # Print downloaded files with full paths
        if result.get("downloaded_files"):
            print("\n📁 Downloaded files:")
            for file_info in result["downloaded_files"]:
                print(f"  📄 {file_info['title']}")
                print(f"     🔗 {file_info['file_path']}")

        print("-" * 50)

    return total_results


def process_categorized_downloads(
    downloader: VideoDownloader, categories: Dict[str, Dict[str, Any]], args
) -> Dict[str, Any]:
    """Process downloads for all categories from YAML config"""
    total_successful = 0
    total_failed = 0
    category_results = {}

    for category_name, category_data in categories.items():
        urls = category_data.get("urls", [])
        if not urls:
            logger.info(f"No URLs in category '{category_name}', skipping...")
            continue

        output_path = category_data.get("output_path", f"./downloads/{category_name}")
        quality = category_data.get("quality", args.quality)
        delay_range = tuple(
            category_data.get("delay_range", [args.delay_min, args.delay_max])
        )

        print(f"\n{'='*60}")
        print(f"📁 Processing Category: {category_name}")
        print(f"📂 Output Path: {output_path}")
        print(f"📊 URLs: {len(urls)}")
        print(f"🎯 Quality: {quality}")
        print(f"⏱️  Delay Range: {delay_range[0]}-{delay_range[1]}s")
        print(f"{'='*60}")

        if args.info_only:
            # Just extract info for this category
            for i, url in enumerate(urls, 1):
                info = downloader.get_video_info(url)
                # print(f"\n{'='*80}")
                # print("RAW INFO OBJECT:")
                # print(f"{'='*80}")
                # print(json.dumps(info, indent=2, ensure_ascii=False, default=str))
                # print(f"{'='*80}")
                if info:
                    print(f"\n[{category_name}] Video {i}/{len(urls)}")
                    print(f"Title: {info.get('title', 'N/A')}")
                    print(f"Season: {info.get('season', 'N/A')}")
                    duration = info.get("duration")
                    if duration is not None:
                        minutes = int(duration) // 60
                        seconds = int(duration) % 60
                        print(f"Duration: {minutes}m {seconds}s")
                    else:
                        print("Duration: N/A")
                    print(f"URL: {url}")
                    print("-" * 50)
        else:
            # Create category-specific config
            category_config = downloader.config.copy()

            # Apply category-specific settings
            if category_data.get("extract_audio", False):
                category_config["extractaudio"] = True
                category_config["audioformat"] = category_data.get(
                    "audio_format", "mp3"
                )

            if "subtitle_langs" in category_data:
                category_config["subtitleslangs"] = category_data["subtitle_langs"]

            if category_data.get("embed_thumbnail", False):
                category_config["embedthumbnail"] = True

            # Create temporary downloader with category config
            temp_downloader = VideoDownloader(category_config)

            # Download videos for this category
            result = temp_downloader.download_videos(
                urls, output_path, quality, delay_range, args.dry_run
            )

            category_results[category_name] = result
            total_successful += len(result["successful"])
            total_failed += len(result["failed"])

            # Print category summary
            print(f"\n📋 Category '{category_name}' Summary:")
            print(f"✅ Successful: {len(result['successful'])}")
            if len(result["failed"]) > 0:
                print(f"❌ Failed: {len(result['failed'])}")

            # Print downloaded files with full paths
            if result.get("downloaded_files"):
                print("\n📁 Downloaded files:")
                for file_info in result["downloaded_files"]:
                    print(f"  📄 {file_info['title']}")
                    print(f"     🔗 {file_info['file_path']}")

            if result["failed"]:
                print(f"\n❌ Failed downloads in '{category_name}':")
                for url in result["failed"]:
                    print(f"  - {url}")

    if not args.info_only:
        # Print overall summary
        print(f"\n{'='*60}")
        print("🎯 OVERALL DOWNLOAD SUMMARY")
        print(f"{'='*60}")
        print(
            f"📁 Categories processed: {len([c for c in categories.values() if c.get('urls')])}"
        )
        print(f"✅ Total successful: {total_successful}")
        if (total_failed) > 0:
            print(f"❌ Total failed: {total_failed}")
        print(f"{'='*60}")

    return {
        "successful": total_successful,
        "failed": total_failed,
        "category_results": category_results,
    }


def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(
        description="Enhanced video downloader using yt-dlp"
    )
    parser.add_argument("urls", nargs="*", help="Video URLs to download")
    parser.add_argument(
        "-f",
        "--file",
        help="YAML config file with URLs and settings (auto-detects config/urls.yaml if not specified)",
    )
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
        default=15,
        help="Maximum delay between downloads (seconds)",
    )
    parser.add_argument(
        "--info-only", action="store_true", help="Extract video info only (no download)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be downloaded without actually downloading",
    )
    parser.add_argument(
        "--config",
        help="YAML config file for yt-dlp options (auto-detects config/config.yaml if not specified)",
    )

    args = parser.parse_args()

    # Load configuration if provided or auto-detect config.yaml
    config = {}
    config_file = args.config

    # Auto-detect config.yaml from config directory only
    if not config_file:
        config_file = "config/config.yaml"
        if os.path.exists(config_file):
            logger.info(f"Auto-detected config file: {config_file}")
        else:
            config_file = None

    # Load the config file if found
    if config_file and os.path.exists(config_file):
        try:
            config = parse_config_file(config_file)
            if config:
                logger.info(
                    f"Loaded {len(config)} configuration options from {config_file}"
                )
        except Exception as e:
            logger.error(f"Error loading config file {config_file}: {e}")

    # Get URLs
    urls = args.urls or []
    categories = {}

    if args.file:
        # Load YAML config file
        categories = load_categorized_urls(args.file)
        if categories:
            logger.info(f"Loaded YAML config with {len(categories)} categories")
    elif not urls:
        # Auto-detect urls.yaml from config directory only if no URLs provided
        config_urls_file = "config/urls.yaml"
        if os.path.exists(config_urls_file):
            logger.info(f"Auto-detected URLs file: {config_urls_file}")
            categories = load_categorized_urls(config_urls_file)
            if categories:
                logger.info(f"Loaded YAML config with {len(categories)} categories")

    if not urls and not categories:
        logger.error("No URLs provided. Use --help for usage information.")
        return

    # Initialize downloader
    downloader = VideoDownloader(config)

    if categories:
        # Process categories from YAML config
        result = process_categorized_downloads(downloader, categories, args)
    else:
        # Standard mode (non-categorized URLs)
        if args.info_only:
            # Just extract info
            for url in urls:
                info = downloader.get_video_info(url)
                if info:
                    # Print raw info object for debugging
                    print(f"\n{'='*80}")
                    print("RAW INFO OBJECT:")
                    print(f"{'='*80}")
                    print(json.dumps(info, indent=2, ensure_ascii=False, default=str))
                    print(f"{'='*80}")

                    print(f"\nTitle: {info.get('title', 'N/A')}")
                    print(f"season: {info.get('season', 'N/A')}")
                    print(f"series: {info.get('series', 'N/A')}")
                    print(f"URL: {url}")
                    print("-" * 50)
        else:
            # Download videos
            result = downloader.download_videos(
                urls,
                args.output,
                args.quality,
                (args.delay_min, args.delay_max),
                args.dry_run,
            )

            # Print summary
            print(f"\n{'='*50}")
            if args.dry_run:
                print("Dry Run Summary:")
                print(f"Would download: {len(result['successful'])}")
            else:
                print("Download Summary:")
                print(f"Successful: {len(result['successful'])}")
            if len(result["failed"]) > 0:
                print(f"Failed: {len(result['failed'])}")

            # Print downloaded files with full paths
            if result.get("downloaded_files"):
                if args.dry_run:
                    print("\n📁 Would download files:")
                else:
                    print("\n📁 Downloaded files:")
                for file_info in result["downloaded_files"]:
                    print(f"  📄 {file_info['title']}")
                    print(f"     🔗 {file_info['file_path']}")

            if result["failed"]:
                if args.dry_run:
                    print("\nFailed simulations:")
                else:
                    print("\nFailed downloads:")
                for url in result["failed"]:
                    print(f"  - {url}")


if __name__ == "__main__":
    main()
