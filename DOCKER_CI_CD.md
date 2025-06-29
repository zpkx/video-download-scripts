# Docker CI/CD with GitHub Actions

这个项目配置了 GitHub Actions 来自动构建和发布 Docker 镜像。

## 🚀 自动化构建

### 触发条件

GitHub Action 会在以下情况下自动运行：

1. **推送到主分支** (`main` 或 `master`)
2. **创建标签** (格式：`v*`，如 `v1.0.0`)
3. **Pull Request** 到主分支

### 构建的镜像

- **镜像名称**: `ghcr.io/{你的用户名}/{仓库名}/video-download-watcher`
- **支持平台**: `linux/amd64`, `linux/arm64`
- **标签策略**:
  - `latest` - 最新的主分支构建
  - `main` 或 `master` - 分支名称
  - `v1.0.0` - 版本标签（如果推送了版本标签）
  - `v1.0`, `v1` - 主要和次要版本标签

## 📦 使用预构建镜像

### 1. 从 GitHub Container Registry 拉取

```bash
# 拉取最新版本
docker pull ghcr.io/{你的用户名}/{仓库名}/video-download-watcher:latest

# 拉取特定版本
docker pull ghcr.io/{你的用户名}/{仓库名}/video-download-watcher:v1.0.0
```

### 2. 更新 docker-compose.yml

你可以修改 `docker-compose.yml` 来使用预构建的镜像而不是本地构建：

```yaml
services:
  video-video-download-watcher:
    image: ghcr.io/{你的用户名}/{仓库名}/video-download-watcher:latest
    # 移除或注释掉 'build: .' 这一行
    container_name: video-video-download-watcher
    volumes:
      - ./downloads:/app/downloads
      - ./config:/app/config
    environment:
      - PYTHONUNBUFFERED=1
    working_dir: /app
    entrypoint: ["/bin/bash"]
    command: ["/app/watch-and-download.sh"]
    restart: unless-stopped
```

### 3. 直接运行容器

```bash
# 运行文件监控器
docker run -d \
  --name video-video-download-watcher \
  -v $(pwd)/downloads:/app/downloads \
  -v $(pwd)/config:/app/config \
  ghcr.io/{你的用户名}/{仓库名}/video-download-watcher:latest \
  /bin/bash /app/watch-and-download.sh

# 运行单次下载
docker run --rm \
  -v $(pwd)/downloads:/app/downloads \
  -v $(pwd)/config:/app/config \
  ghcr.io/{你的用户名}/{仓库名}/video-download-watcher:latest \
  -f /app/config/urls.yaml
```

## 🔧 配置说明

### GitHub Packages 权限

GitHub Action 使用 `GITHUB_TOKEN` 来推送镜像到 GitHub Container Registry (ghcr.io)。这个 token 会自动提供，无需额外配置。

### 私有仓库访问

如果你的仓库是私有的，你需要：

1. 创建个人访问令牌 (PAT)
2. 登录到 GitHub Container Registry：
   ```bash
   echo $CR_PAT | docker login ghcr.io -u USERNAME --password-stdin
   ```

### 自定义构建

如果需要自定义构建过程，可以修改 `.github/workflows/docker-image.yml` 文件：

- 更改触发条件
- 添加额外的测试步骤
- 修改标签策略
- 添加其他注册表

## 📋 工作流程详情

### 构建步骤

1. **检出代码** - 下载仓库代码
2. **设置 Docker Buildx** - 启用多平台构建
3. **登录容器注册表** - 认证到 ghcr.io
4. **提取元数据** - 生成标签和标签
5. **构建和推送** - 构建镜像并推送到注册表

### 测试步骤

1. **拉取镜像** - 验证镜像已成功推送
2. **基础功能测试** - 运行 `--help` 命令
3. **Docker Compose 验证** - 检查配置文件语法

## 🔍 监控构建

你可以在 GitHub 仓库的 "Actions" 标签页中查看构建状态：

- 绿色勾号 ✅ - 构建成功
- 红色叉号 ❌ - 构建失败
- 黄色圆圈 🟡 - 构建进行中

## 🏷️ 版本发布

要发布新版本：

1. 创建并推送版本标签：
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. GitHub Action 会自动构建并发布新版本的镜像

3. 你可以在 GitHub 包页面查看发布的镜像：
   `https://github.com/{你的用户名}/{仓库名}/pkgs/container/video-download-watcher`

## 🛠️ 故障排除

### 构建失败

如果构建失败，检查：
- Dockerfile 语法是否正确
- 所有必需的文件是否存在
- 依赖项是否可以正常安装

### 权限问题

如果遇到权限错误：
- 确保 GitHub Actions 有写入包的权限
- 检查仓库设置中的包权限配置

### 镜像拉取失败

如果无法拉取镜像：
- 检查镜像名称和标签是否正确
- 确保你有访问包的权限（对于私有镜像）
