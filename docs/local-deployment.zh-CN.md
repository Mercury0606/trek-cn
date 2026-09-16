# TREK CN 中文本地部署说明

## 1. 目录结构

建议把部署文件放在一个独立目录中：

```text
trek/
├── docker-compose.yml
├── .env
├── data/       # 数据库、账户、日志和密钥
└── uploads/    # 照片、视频和附件
```

不要把已有安装的 `data/` 或 `uploads/` 与新的试用实例混用。

## 2. 最小配置

Compose 服务至少需要以下设置：

```yaml
services:
  app:
    image: mauriceboe/trek:4.2.1
    ports:
      - "127.0.0.1:3000:3000"
    environment:
      - NODE_ENV=production
      - PORT=3000
      - ENCRYPTION_KEY=${ENCRYPTION_KEY}
      - TZ=${TZ:-Asia/Shanghai}
      - DEFAULT_LANGUAGE=${DEFAULT_LANGUAGE:-zh}
    volumes:
      - ./data:/app/data
      - ./uploads:/app/uploads
    restart: unless-stopped
```

生成密钥后写入 `.env`：

```dotenv
ENCRYPTION_KEY=请替换为openssl rand -hex 32的输出
TZ=Asia/Shanghai
DEFAULT_LANGUAGE=zh
```

AI、OIDC、MCP、HTTPS 等功能保持关闭即可完成基础试用，因此不需要 AI API Key。

## 3. 首次登录

启动后访问 <http://localhost:3000>。如需固定首次管理员账户，可在首次启动前增加：

```yaml
environment:
  - ADMIN_EMAIL=admin@example.local
  - ADMIN_PASSWORD=请设置一个临时强密码
```

这两个值只在实例没有用户时使用。登录后应立即改成个人密码；不要把真实密码提交到 GitHub。

## 4. 地图覆盖的边界

TREK 默认 Atlas 数据来自上游构建流程。中国专用 GeoJSON 的来源、授权和地图合规状态未确认前，只建议在本机挂载，不建议制作公开镜像。

本地挂载的原则是：

- 只覆盖 Atlas 数据，不改动 `data/` 和 `uploads/`；
- 保留原始数据副本，记录来源、下载日期和许可证；
- 公开部署前，确认数据允许再分发，并按要求处理审图号、备案和底图归属；
- 不使用“把 Ladakh 归入中国”这种属性改写来修复边界显示；需要的是独立的中国 GeoJSON 图层。

## 5. 验收清单

- 首页可以打开，管理员可以登录；
- 可以创建行程、地点、日程和费用；
- 可以上传照片或附件；
- 重启容器后数据仍在；
- 浏览器语言切换到简体中文后，主要界面显示中文；
- 地图数据的来源和许可记录完整。

