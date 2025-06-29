# 快速使用指南

## 启动文件监控服务

1. **第一次使用**
   ```bash
   ./start-watcher.sh
   ```
   这会自动创建必要的目录和示例配置文件。

2. **编辑配置文件**
   编辑 `config/urls.yaml` 文件，添加你要下载的视频链接：
   ```yaml
   categories:
     凡人修仙传:
       output_path: "./downloads/凡人修仙传"
       urls:
         - https://www.bilibili.com/bangumi/play/ep1231557/
   ```

3. **保存文件**
   一旦保存 `config/urls.yaml` 文件，监控服务会自动检测到变化并开始下载。

## 其他有用的命令

- **停止服务**: `Ctrl+C` 或 `docker-compose down`
- **重新构建**: `docker-compose build`
- **查看日志**: `docker-compose logs video-download-watcher`
- **单次下载**: `docker-compose run --rm video-downloader-oneshot -f /app/config/urls.yaml`

## 文件结构

```
├── config/
│   ├── urls.yaml          # 视频链接配置
│   ├── config.yaml        # 下载设置（可选）
│   └── cookies.txt        # Cookie文件（可选）
├── downloads/             # 下载文件存储位置
├── start-watcher.sh       # 启动监控服务脚本
└── docker-compose.yml     # Docker配置
```

## 注意事项

- 监控服务会在启动时执行一次初始下载
- 每次修改 `urls.yaml` 后会有2秒延迟才开始下载，确保文件完全写入
- 下载的视频会保存到 `downloads/` 目录中相应的分类文件夹
- 服务会持续运行，可以随时修改 `urls.yaml` 文件添加新的下载任务
