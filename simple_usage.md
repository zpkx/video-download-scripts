# 简化版视频下载器使用示例

## 基本用法

### 1. 下载单个视频
```bash
python simple_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### 2. 下载多个视频
```bash
python simple_downloader.py "URL1" "URL2" "URL3"
```

### 3. 从文件读取URL列表
```bash
python simple_downloader.py -f urls.txt
```

### 4. 指定输出目录
```bash
python simple_downloader.py -o /path/to/downloads "URL"
```

### 5. 选择视频质量
```bash
python simple_downloader.py -q 720p "URL"
python simple_downloader.py -q 480p "URL"
python simple_downloader.py -q best "URL"  # 默认
```

### 6. 只获取视频信息，不下载
```bash
python simple_downloader.py --info "URL"
```

## URL文件格式

创建一个 `urls.txt` 文件，每行一个URL：

```
https://www.youtube.com/watch?v=VIDEO_ID1
https://www.youtube.com/watch?v=VIDEO_ID2
# 这是注释，会被忽略
https://www.youtube.com/watch?v=VIDEO_ID3
```

## Cookies支持

如果需要下载需要登录的视频，可以将cookies文件放在以下位置：
- `config/cookies.txt`
- `cookies.txt`
- `~/cookies.txt`

## 与原版的主要区别

### 简化的功能：
- 移除了复杂的YAML配置系统
- 移除了分类下载功能
- 移除了复杂的延迟配置
- 简化了日志输出
- 移除了FFmpeg自动检测

### 保留的核心功能：
- 基本视频下载
- 质量选择（best/720p/480p）
- 从文件读取URL
- 错误处理
- Cookies支持
- 视频信息获取

### 优势：
- 代码更简洁（约150行 vs 原来700+行）
- 更容易理解和维护
- 启动更快
- 适合大多数基本使用场景
