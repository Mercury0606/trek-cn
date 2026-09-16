# TREK CN VPS 部署路线

这份说明以当前本地试用版本为基础：官方 `mauriceboe/trek:4.2.1` 镜像，加上 `deploy/custom-frontend/` 中的前端覆盖文件和使用者自行准备的 Atlas GeoJSON。公开仓库不包含账户数据、行程、上传文件、`.env` 或未确认许可的地图原始数据。

## 1. 建议的服务器目录

```text
/opt/trek-cn/
├── docker-compose.yml
├── .env
├── data/
├── uploads/
├── custom-atlas/
└── custom-frontend/
```

把仓库 `deploy/docker-compose.local-cn.template.yml` 复制为服务器上的 `docker-compose.yml`，再把对应版本的前端覆盖文件复制到 `custom-frontend/`。如果要使用中国地图覆盖，还要把有权使用的 `admin0.geojson.gz` 和 `admin1.geojson.gz` 放到 `custom-atlas/`。

当前版本的地图资产可以从 [v4.2.1-cn.4](https://github.com/Mercury0606/trek-cn/releases/tag/v4.2.1-cn.4) 下载：

```bash
curl -fL https://github.com/Mercury0606/trek-cn/releases/download/v4.2.1-cn.4/admin0.geojson.gz -o custom-atlas/admin0.geojson.gz
curl -fL https://github.com/Mercury0606/trek-cn/releases/download/v4.2.1-cn.4/admin1.geojson.gz -o custom-atlas/admin1.geojson.gz
shasum -a 256 custom-atlas/admin0.geojson.gz custom-atlas/admin1.geojson.gz
```

下载后应得到以下哈希：

```text
fb4514e70c4314c3dd15bdb5136a0a29e00dc5031db41f76c8dd3b82caa5c0f3  custom-atlas/admin0.geojson.gz
b972a19c8f22fac41f8d8228816515e2daeaf8a91f882148283f0b2f7318d68b  custom-atlas/admin1.geojson.gz
```

## 2. 首次上线前的配置

在服务器上生成新的加密密钥：

```bash
openssl rand -hex 32
```

创建 `.env`，至少包含：

```dotenv
ENCRYPTION_KEY=服务器专用的64位十六进制字符串
TZ=Asia/Shanghai
DEFAULT_LANGUAGE=zh
TREK_PORT=3000
```

不要复用本机密钥，也不要把 `.env` 提交到 GitHub。首次启动可临时设置 `ADMIN_EMAIL` 和 `ADMIN_PASSWORD`；登录后立即更换密码，并从部署文件或环境管理器中移除明文密码。

## 3. 第一次验证

第一阶段只绑定 VPS 本机端口。可以从自己的电脑通过 SSH 隧道访问：

```bash
ssh -L 3000:127.0.0.1:3000 user@your-vps
```

然后在本机浏览器打开 <http://localhost:3000>，验证登录、创建行程、费用、上传文件和重启保留数据。

服务器上常用操作：

```bash
docker compose config
docker compose up -d
docker compose ps
docker compose logs -f
docker compose restart
docker compose stop
```

## 4. 域名和 HTTPS

本机验证通过后，再让域名指向 VPS，并使用 Caddy、Nginx 或现有网关终止 TLS。反向代理只应转发到 `127.0.0.1:3000`；不要直接把应用端口暴露到公网。

配置域名后，把 `ALLOWED_ORIGINS` 改为实际的 HTTPS 地址，例如：

```dotenv
ALLOWED_ORIGINS=https://trek.example.com
```

如启用 HTTPS 相关环境变量或 OIDC，请按照上游文档同时配置 `APP_URL`、代理信任和安全 Cookie。没有域名和证书时，不要提前打开 `FORCE_HTTPS`。

## 5. 备份和升级

至少备份：

- `data/`：数据库、账户、设置和密钥相关数据；
- `uploads/`：照片、视频和附件；
- `.env`：加密密钥必须安全保存，否则备份可能无法恢复。

升级时先备份，再拉取新镜像并重建容器；不要删除这三个持久化对象。恢复前先停掉应用，并在副本目录验证备份。

## 6. 中国地图覆盖的发布边界

当前中国 GeoJSON 只作为本地/VPS 私有覆盖，原因是数据来源、再分发许可以及公开地图的审图/备案要求尚未完成确认。公开部署前，应单独完成：

1. 数据来源和许可证核验；
2. 底图服务和边界数据归属标注；
3. 公开展示所需的审图、备案或其他合规流程；
4. 与 TREK 版本匹配的前端资源和 GeoJSON 回归测试。

地图覆盖只改变显示图层，不把 Ladakh 等地区的数据库属性迁移到中国，也不改变已有访问记录的代码。
