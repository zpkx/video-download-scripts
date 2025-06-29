#!/bin/bash

# 测试 UID/GID 配置的脚本

set -e

echo "🧪 测试 Docker UID/GID 配置...echo "💡 使用建议:"
echo "   1. 运行 './setup-env.sh' 设置环境变量"
echo "   2. 使用 'docker-compose up -d video-downloader-watcher' 启动服务"
echo "   3. 检查 downloads/ 目录中文件的权限是否正确"
echo "   4. 检查 logs/ 目录中的日志文件"ho ""

# 检查是否存在 .env 文件
if [ -f .env ]; then
    echo "✅ 找到 .env 文件"
    echo "   内容:"
    cat .env | grep -E "USER_(UID|GID)" | sed 's/^/   /'
else
    echo "⚠️  未找到 .env 文件"
    echo "   运行 './setup-env.sh' 来创建"
fi

echo ""

# 获取当前用户信息
echo "📋 当前用户信息:"
echo "   UID: $(id -u)"
echo "   GID: $(id -g)"
echo "   用户名: $(whoami)"

echo ""

# 测试构建
echo "🔨 测试 Docker 构建 (使用当前用户 UID/GID)..."
USER_UID=$(id -u) USER_GID=$(id -g) docker-compose build video-downloader --quiet

if [ $? -eq 0 ]; then
    echo "✅ Docker 构建成功"
else
    echo "❌ Docker 构建失败"
    exit 1
fi

echo ""

# 测试权限
echo "🔒 测试文件权限..."
mkdir -p test-downloads test-config test-logs

# 创建测试配置
echo "urls: []" > test-config/urls.yaml

# 运行容器测试权限
USER_UID=$(id -u) USER_GID=$(id -g) docker run --rm \
    -v $(pwd)/test-downloads:/app/downloads \
    -v $(pwd)/test-config:/app/config \
    -v $(pwd)/test-logs:/app/logs \
    --user "$(id -u):$(id -g)" \
    video-downloader:local \
    bash -c "touch /app/downloads/test-file.txt && touch /app/logs/test-log.txt"

if [ -f test-downloads/test-file.txt ] && [ -f test-logs/test-log.txt ]; then
    echo "✅ 文件权限测试通过"
    echo "   创建的下载文件所有者: $(ls -la test-downloads/test-file.txt | awk '{print $3":"$4}')"
    echo "   创建的日志文件所有者: $(ls -la test-logs/test-log.txt | awk '{print $3":"$4}')"
    echo "   当前用户: $(whoami):$(id -gn)"
else
    echo "❌ 文件权限测试失败"
fi

# 清理测试文件
rm -rf test-downloads test-config test-logs

echo ""
echo "🎉 测试完成!"
echo ""
echo "💡 使用建议:"
echo "   1. 运行 './setup-env.sh' 设置环境变量"
echo "   2. 使用 'docker-compose up -d video-download-watcher' 启动服务"
echo "   3. 检查 downloads/ 目录中文件的权限是否正确"
