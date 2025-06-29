#!/usr/bin/env python3
"""
简化版视频下载器 - 使用 yt-dlp
保留核心功能，简化复杂的配置和分类系统
"""

import yt_dlp
import os
import argparse
import logging
from typing import List, Optional, Dict, Any
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class SimpleVideoDownloader:
    """简化的视频下载器"""

    def __init__(self):
        self.default_opts = {
            "format": "best[height<=720]",  # 默认720p或以下最佳质量
            "outtmpl": "%(title)s.%(ext)s",  # 输出文件名模板
            "ignoreerrors": True,  # 忽略错误继续下载
        }

    def download_videos(
        self,
        urls: List[str],
        output_dir: str = "./downloads",
        quality: str = "best"
    ) -> Dict[str, List[str]]:
        """
        下载视频列表

        Args:
            urls: 视频URL列表
            output_dir: 下载目录
            quality: 视频质量 (best/720p/480p)

        Returns:
            包含成功和失败URL的字典
        """
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)

        # 配置下载选项
        opts = self.default_opts.copy()
        opts["outtmpl"] = os.path.join(output_dir, opts["outtmpl"])

        # 设置质量
        if quality == "720p":
            opts["format"] = "best[height<=720]"
        elif quality == "480p":
            opts["format"] = "best[height<=480]"
        elif quality == "best":
            opts["format"] = "best"

        # 查找cookies文件
        cookies_file = self._find_cookies()
        if cookies_file:
            opts["cookiefile"] = cookies_file

        successful = []
        failed = []

        with yt_dlp.YoutubeDL(opts) as ydl:
            for i, url in enumerate(urls, 1):
                try:
                    logger.info(f"下载 {i}/{len(urls)}: {url}")
                    ydl.download([url])
                    successful.append(url)
                    logger.info(f"下载成功: {url}")

                    # 短暂延迟避免限流
                    if i < len(urls):
                        time.sleep(2)

                except Exception as e:
                    logger.error(f"下载失败 {url}: {e}")
                    failed.append(url)

        return {"successful": successful, "failed": failed}

    def get_video_info(self, url: str) -> Optional[Dict[str, Any]]:
        """获取视频信息"""
        opts = {"quiet": True, "no_warnings": True}

        # 添加cookies如果存在
        cookies_file = self._find_cookies()
        if cookies_file:
            opts["cookiefile"] = cookies_file

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
        except Exception as e:
            logger.error(f"获取视频信息失败 {url}: {e}")
            return None

    def _find_cookies(self) -> Optional[str]:
        """查找cookies文件"""
        possible_paths = [
            "config/cookies.txt",
            "cookies.txt",
            os.path.expanduser("~/cookies.txt"),
        ]

        for path in possible_paths:
            if os.path.exists(path):
                logger.info(f"找到cookies文件: {path}")
                return path
        return None


def load_urls_from_file(file_path: str) -> List[str]:
    """从文件加载URL列表"""
    urls = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    urls.append(line)
        logger.info(f"从 {file_path} 加载了 {len(urls)} 个URL")
    except Exception as e:
        logger.error(f"加载URL文件错误: {e}")
    return urls


def main():
    """主程序"""
    parser = argparse.ArgumentParser(description="简化版视频下载器")
    parser.add_argument("urls", nargs="*", help="视频URL")
    parser.add_argument("-f", "--file", help="包含URL的文本文件")
    parser.add_argument("-o", "--output", default="./downloads", help="输出目录")
    parser.add_argument(
        "-q", "--quality",
        choices=["best", "720p", "480p"],
        default="best",
        help="视频质量"
    )
    parser.add_argument("--info", action="store_true", help="只获取视频信息，不下载")

    args = parser.parse_args()

    # 获取URL列表
    urls = list(args.urls) if args.urls else []

    if args.file:
        urls.extend(load_urls_from_file(args.file))

    # 如果没有URL，尝试查找默认URL文件
    if not urls:
        default_files = ["urls.txt", "config/urls.txt"]
        for file_path in default_files:
            if os.path.exists(file_path):
                urls.extend(load_urls_from_file(file_path))
                break

    if not urls:
        logger.error("没有提供URL。使用 --help 查看使用说明")
        return

    # 初始化下载器
    downloader = SimpleVideoDownloader()

    if args.info:
        # 只获取信息
        for url in urls:
            info = downloader.get_video_info(url)
            if info:
                title = info.get("title", "未知标题")
                duration = info.get("duration")
                duration_str = f"{duration//60}:{duration % 60:02d}" if duration else "未知"
                print(f"标题: {title}")
                print(f"时长: {duration_str}")
                print(f"URL: {url}")
                print("-" * 50)
    else:
        # 下载视频
        print(f"开始下载 {len(urls)} 个视频到 {args.output}")
        result = downloader.download_videos(urls, args.output, args.quality)

        # 显示结果
        print(f"\n下载完成!")
        print(f"成功: {len(result['successful'])}")
        if result["failed"]:
            print(f"失败: {len(result['failed'])}")
            print("失败的URL:")
            for url in result["failed"]:
                print(f"  - {url}")


if __name__ == "__main__":
    main()
