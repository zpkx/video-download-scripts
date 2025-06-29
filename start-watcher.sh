#!/bin/bash

echo "🎬 启动视频下载监控服务..."
echo "===================="
echo "此服务会监控 config/urls.yaml 文件的变化"
echo "当文件被修改后，会自动开始下载视频"
echo "===================="

# 确保 downloads 目录存在
mkdir -p downloads

# 确保 config 目录存在
mkdir -p config

# 如果 config/urls.yaml 不存在，创建一个示例文件
if [ ! -f "config/urls.yaml" ]; then
    echo "📝 创建示例 config/urls.yaml 文件..."
    cat > config/urls.yaml << 'EOF'
# 视频下载配置文件 (YAML格式)
categories:
  示例视频:
    output_path: "./downloads/示例视频"
    urls:
      # 请在这里添加你要下载的视频链接
      # - https://example.com/video1
      # - https://example.com/video2
EOF
    echo "✅ 已创建 config/urls.yaml，请编辑此文件添加你的视频链接"
    echo ""
fi

# 构建并启动服务
echo "🏗️  构建 Docker 镜像..."
docker compose build video-downloader-watcher

if [ $? -eq 0 ]; then
    echo ""
    echo "🚀 启动文件监控服务..."
    echo "💡 提示: 编辑 config/urls.yaml 文件会自动触发下载"
    echo "🛑 按 Ctrl+C 停止服务"
    echo ""
    docker compose up video-downloader-watcher
else
    echo "❌ 构建失败，请检查错误信息"
    exit 1
fi

echo ""
echo "🔴 服务已停止"
