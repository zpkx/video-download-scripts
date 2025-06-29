# 视频下载器简化对比

## 简化前后对比

### 代码行数对比
- **原版**: ~725行
- **简化版**: ~150行
- **减少**: 约80%的代码量

### 功能对比

| 功能 | 原版 | 简化版 | 说明 |
|------|------|--------|------|
| 基本视频下载 | ✅ | ✅ | 核心功能保留 |
| 质量选择 | ✅ | ✅ | 简化为3个选项 |
| 批量下载 | ✅ | ✅ | 从文件或命令行 |
| Cookies支持 | ✅ | ✅ | 自动查找cookies文件 |
| 错误处理 | ✅ | ✅ | 基本错误处理 |
| 视频信息获取 | ✅ | ✅ | --info参数 |
| YAML配置 | ✅ | ❌ | 移除复杂配置 |
| 分类下载 | ✅ | ❌ | 移除分类功能 |
| 复杂延迟配置 | ✅ | ❌ | 固定2秒延迟 |
| FFmpeg自动检测 | ✅ | ❌ | 依赖系统PATH |
| 详细日志输出 | ✅ | ❌ | 简化日志 |
| 进度钩子 | ✅ | ❌ | 移除复杂进度跟踪 |

### 配置文件对比

#### 原版配置（复杂）
```yaml
# config/config.yaml
format: "bestvideo[height>=720]+bestaudio/best"
writesubtitles: true
subtitleslangs: ["zh-CN", "zh-TW", "en"]
embed_subs: true
# ... 更多配置项

# config/urls.yaml  
categories:
  电影:
    urls:
      - "https://example.com/movie1"
    output_path: "./downloads/movies"
    quality: "high"
  电视剧:
    urls:
      - "https://example.com/tv1"
    output_path: "./downloads/tv"
```

#### 简化版配置（简单）
```bash
# urls.txt
https://example.com/video1
https://example.com/video2
# 注释
https://example.com/video3
```

### 使用方式对比

#### 原版使用
```bash
# 复杂的命令行选项
python video_downloader.py -f config/urls.yaml --config config/config.yaml --quality high --delay-seconds 5 --delay-max 15

# 或者依赖自动检测
python video_downloader.py
```

#### 简化版使用
```bash
# 简单直接
python simple_downloader.py -f urls.txt -q 720p -o downloads

# 或者直接指定URL
python simple_downloader.py "URL1" "URL2"
```

## 简化版的优势

### 1. **易于理解**
- 代码结构清晰
- 功能单一明确
- 新手友好

### 2. **维护简单**
- 减少了80%的代码
- 移除了复杂的依赖关系
- 错误排查更容易

### 3. **性能更好**
- 启动速度更快
- 内存使用更少
- 减少了不必要的功能开销

### 4. **使用方便**
- 命令行参数简化
- 不需要复杂的配置文件
- 满足大部分使用场景

## 什么时候使用哪个版本？

### 使用简化版的场景：
- 个人日常下载视频
- 简单的批量下载
- 学习yt-dlp使用
- 快速下载少量视频
- 不需要复杂分类管理

### 使用原版的场景：
- 需要详细的下载分类
- 复杂的配置需求
- 大规模自动化下载
- 需要详细的进度跟踪
- 企业级使用场景

## 迁移建议

如果你当前使用原版，想切换到简化版：

1. **备份当前配置**
2. **提取URL列表**到simple的txt格式
3. **测试简化版**是否满足需求
4. **逐步迁移**，保留原版作为备份
