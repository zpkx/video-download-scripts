#!/bin/bash

# 自动设置 UID/GID 环境变量的脚本

set -e

# 获取当前用户的 UID 和 GID
USER_UID=$(id -u)
USER_GID=$(id -g)

echo "检测到的用户信息:"
echo "  UID: $USER_UID"
echo "  GID: $USER_GID"

# 创建或更新 .env 文件
echo "创建 .env 文件..."
cat > .env << EOF
# Docker 环境变量 - 自动生成
# 生成时间: $(date)

# 用户 UID 和 GID (避免文件权限问题)
USER_UID=$USER_UID
USER_GID=$USER_GID
EOF

echo "✅ .env 文件已创建/更新"
echo ""
echo "现在你可以使用以下命令:"
echo "  docker-compose up -d video-download-watcher  # 启动文件监控器"
echo "  docker-compose run --rm video-downloader     # 运行一次性下载"
echo ""
echo "或者使用环境变量直接运行:"
echo "  USER_UID=$USER_UID USER_GID=$USER_GID docker-compose up -d"
