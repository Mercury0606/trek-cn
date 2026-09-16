# TREK CN

这是 [TREK](https://github.com/liketrek/TREK) 的中文社区 Fork，仓库名为 `trek-cn`。

本项目用于在中文环境下试用和维护 TREK。它不是 TREK 官方发行版，也不代表上游项目立场；上游代码、商标和第三方数据仍按各自的许可证与归属要求使用。本仓库遵循上游的 [AGPL-3.0](./LICENSE) 许可证。

## 当前版本

- 基础版本：TREK v4.2.1
- 中文界面：沿用上游 `zh`（简体中文）语言包，并以中文作为中文部署的推荐默认语言
- 地图：公开仓库保留上游合规地图资源；中国口径的 GeoJSON 仅作为本地试用数据，不随公开镜像发布
- AI：默认关闭，不需要 AI API Key 或 Ollama

## 本机试用

建议使用 Docker Compose，并将数据放在独立目录：

```bash
mkdir -p data uploads
openssl rand -hex 32
```

在 `.env` 中填写生成的密钥：

```dotenv
ENCRYPTION_KEY=替换为上一步生成的64位十六进制字符串
TZ=Asia/Shanghai
DEFAULT_LANGUAGE=zh
```

本机端口建议绑定到回环地址：

```yaml
ports:
  - "127.0.0.1:3000:3000"
```

然后启动：

```bash
docker compose up -d
```

打开 <http://localhost:3000>。首次启动可以通过 `ADMIN_EMAIL` 和 `ADMIN_PASSWORD` 指定管理员；如果没有指定，请查看容器首次启动日志中的管理员提示。

常用操作：

```bash
docker compose logs -f
docker compose stop
docker compose start
docker compose down
```

`down` 只删除容器，`data/` 和 `uploads/` 会保留。升级前请先备份这两个目录。

## 中国地图数据说明

公开发布的地图必须同时考虑数据许可证、边界表达准确性、审图/备案以及底图服务条款。当前本 Fork 不把来源和再分发许可尚未确认的中国 GeoJSON 放入仓库或 GHCR 镜像。

本地试用可以通过 Compose bind mount 覆盖 Atlas 数据目录；数据文件应由使用者自行取得并确认有权使用。不要把本地 `data/`、`uploads/` 或中国专用 GeoJSON 提交到公开仓库。

详见：[中文本地部署与地图覆盖说明](./docs/local-deployment.zh-CN.md)。

## 与上游同步

这是一个 Fork，保留了与 `liketrek/TREK` 的关联。同步上游更新时，请优先检查：

1. `shared/src/i18n/` 是否新增或变更翻译键；
2. `client/src/pages/HelpPage.tsx` 与 `wiki/` 的帮助内容是否需要同步；
3. 地图构建脚本、第三方归属和许可证是否变化；
4. Docker 镜像和默认配置是否仍适合中文本地部署。

## 贡献

欢迎提交中文翻译、帮助文档和本地部署改进。涉及中国地图边界、地图服务或公开镜像的改动，请同时提供数据来源、许可证和合规说明。

