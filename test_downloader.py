#!/usr/bin/env python3
"""
Test script to verify the video downloader functionality
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))


def test_video_downloader():
    """Test the VideoDownloader class without actual downloads"""
    try:
        from video_downloader import VideoDownloader, load_urls_from_file

        print("✓ Successfully imported VideoDownloader")

        # Test initialization
        downloader = VideoDownloader()
        print("✓ VideoDownloader initialized successfully")

        # Test configuration
        config = downloader._get_default_config()
        assert isinstance(config, dict)
        print("✓ Default configuration loaded")

        # Test output template creation
        template = downloader._create_output_template("./test")
        assert "./test" in template
        print("✓ Output template creation works")

        # Test URL loading from file
        with open("test_urls.txt", "w") as f:
            f.write("# Test file\n")
            f.write("https://example.com/video1\n")
            f.write("https://example.com/video2\n")

        urls = load_urls_from_file("test_urls.txt")
        assert len(urls) == 2
        print("✓ URL loading from file works")

        # Cleanup
        os.remove("test_urls.txt")

        print("\n🎉 All tests passed! The video downloader is ready to use.")
        print("To install dependencies, run: pip install -r requirements.txt")

        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install dependencies: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def test_ffmpeg_detection():
    """Test FFmpeg detection functionality"""
    try:
        from video_downloader import VideoDownloader
        import shutil

        print("\n🔧 Testing FFmpeg detection...")

        downloader = VideoDownloader()
        ffmpeg_path = downloader._get_ffmpeg_location()

        if ffmpeg_path:
            print(f"✓ FFmpeg found at: {ffmpeg_path}")

            # Test if ffmpeg is actually executable
            import subprocess
            try:
                result = subprocess.run([ffmpeg_path, "-version"],
                                        capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    version_line = result.stdout.split('\n')[0]
                    print(f"✓ FFmpeg is working: {version_line}")
                else:
                    print(f"⚠️  FFmpeg found but may not be working properly")
            except subprocess.TimeoutExpired:
                print(f"⚠️  FFmpeg found but version check timed out")
            except Exception as e:
                print(f"⚠️  FFmpeg found but error checking version: {e}")
        else:
            print("❌ FFmpeg not found")
            print("📝 To install FFmpeg:")
            print("   - On Ubuntu/Debian: sudo apt update && sudo apt install ffmpeg")
            print("   - On macOS: brew install ffmpeg")
            print("   - On Windows: Download from https://ffmpeg.org/download.html")

        # Also check if it's in PATH using shutil.which
        which_ffmpeg = shutil.which("ffmpeg")
        if which_ffmpeg:
            print(f"✓ FFmpeg also found in PATH: {which_ffmpeg}")
        else:
            print("❌ FFmpeg not found in PATH")

        return ffmpeg_path is not None

    except Exception as e:
        print(f"❌ FFmpeg test failed: {e}")
        return False


def test_cookies_detection():
    """Test cookies file detection functionality"""
    try:
        from video_downloader import VideoDownloader

        print("\n🍪 Testing cookies detection...")

        downloader = VideoDownloader()
        cookies_file = downloader._get_cookies_file()

        if cookies_file:
            print(f"✓ Cookies file found at: {cookies_file}")

            # Check if cookies file is readable and has content
            try:
                with open(cookies_file, 'r') as f:
                    content = f.read().strip()
                    if content:
                        lines = content.split('\n')
                        valid_lines = [
                            line for line in lines if line.strip() and not line.startswith('#')]
                        print(
                            f"✓ Cookies file has {len(valid_lines)} cookie entries")

                        # Check for common cookie formats
                        if any('\t' in line for line in valid_lines):
                            print("✓ Detected Netscape cookie format")
                        elif any('=' in line for line in valid_lines):
                            print("✓ Detected key=value cookie format")
                    else:
                        print("⚠️  Cookies file is empty")
            except Exception as e:
                print(f"⚠️  Error reading cookies file: {e}")
        else:
            print("❌ No cookies file found")
            print("📝 To add cookies:")
            print("   - Create a 'cookies.txt' file in the project directory")
            print("   - Export cookies from your browser using extensions like:")
            print("     * Get cookies.txt LOCALLY (Chrome/Firefox)")
            print("     * cookies.txt (Chrome)")
            print("   - Common locations checked:")
            possible_paths = [
                "cookies.txt",
                "www.bilibili.com_cookies.txt",
                os.path.expanduser("~/cookies.txt"),
                os.path.expanduser("~/Downloads/cookies.txt"),
            ]
            for path in possible_paths:
                print(f"     * {path}")

        return cookies_file is not None

    except Exception as e:
        print(f"❌ Cookies test failed: {e}")
        return False


def create_sample_cookies_file():
    """Create a sample cookies file for testing"""
    try:
        sample_content = """# Netscape HTTP Cookie File
# This is a sample cookies file for testing
# .example.com	TRUE	/	FALSE	1672531200	session_id	sample_session_123
# .bilibili.com	TRUE	/	FALSE	1672531200	SESSDATA	sample_sessdata_456
"""
        with open("sample_cookies.txt", "w") as f:
            f.write(sample_content)
        print("✓ Created sample cookies file: sample_cookies.txt")
        return True
    except Exception as e:
        print(f"❌ Failed to create sample cookies file: {e}")
        return False


def test_integration_with_ffmpeg_and_cookies():
    """Test VideoDownloader with both FFmpeg and cookies configured"""
    try:
        from video_downloader import VideoDownloader

        print("\n🔗 Testing integration with FFmpeg and cookies...")

        # Create a test configuration that would use both
        config = {
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
        }

        downloader = VideoDownloader(config)

        # Test the download configuration setup (without actually downloading)
        ydl_opts = downloader.default_config.copy()
        ydl_opts.update(config)

        # Check if cookies would be configured
        cookies_file = downloader._get_cookies_file()
        if cookies_file:
            ydl_opts["cookiefile"] = cookies_file
            print(f"✓ Cookies would be configured: {cookies_file}")

        # Check if FFmpeg would be configured
        ffmpeg_location = downloader._get_ffmpeg_location()
        if ffmpeg_location:
            ydl_opts["ffmpeg_location"] = os.path.dirname(ffmpeg_location)
            print(
                f"✓ FFmpeg would be configured: {os.path.dirname(ffmpeg_location)}")

        # Test output template creation
        template = downloader._create_output_template("./test_downloads")
        print(f"✓ Output template: {template}")

        print("✓ Integration test passed - downloader configured properly")

        # Show final configuration summary
        print("\n📋 Final yt-dlp configuration summary:")
        important_opts = ["format", "merge_output_format",
                          "cookiefile", "ffmpeg_location"]
        for opt in important_opts:
            if opt in ydl_opts:
                print(f"   {opt}: {ydl_opts[opt]}")

        return True

    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False


def run_comprehensive_tests():
    """Run all tests including FFmpeg and cookies"""
    print("🚀 Running comprehensive video downloader tests...\n")

    results = {
        "basic": test_video_downloader(),
        "ffmpeg": test_ffmpeg_detection(),
        "cookies": test_cookies_detection(),
        "integration": test_integration_with_ffmpeg_and_cookies(),
    }

    print(f"\n{'='*60}")
    print("🎯 Test Results Summary:")
    print(f"{'='*60}")

    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name.capitalize():15} {status}")

    total_passed = sum(results.values())
    total_tests = len(results)

    print(f"\nOverall: {total_passed}/{total_tests} tests passed")

    if total_passed == total_tests:
        print("🎉 All tests passed! Your video downloader is fully configured.")
    else:
        print("⚠️  Some components need attention. Check the details above.")

        # Provide installation suggestions
        if not results["ffmpeg"]:
            print("\n💡 FFmpeg installation suggestions:")
            print("   sudo apt update && sudo apt install ffmpeg  # Ubuntu/Debian")
            print("   brew install ffmpeg                         # macOS")

        if not results["cookies"]:
            print("\n💡 Cookies setup suggestions:")
            print("   1. Install a browser extension to export cookies")
            print("   2. Export cookies for the sites you want to download from")
            print("   3. Save as 'cookies.txt' in the project directory")

    return total_passed == total_tests


if __name__ == "__main__":
    run_comprehensive_tests()
