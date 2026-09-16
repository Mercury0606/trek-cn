# 中国地图数据来源与合规声明

## 数据用途

本目录中的两个压缩 GeoJSON 是 TREK Atlas 的实验性显示覆盖文件：

- `admin0.geojson.gz`：国家级显示轮廓；
- `admin1.geojson.gz`：省级显示轮廓。

它们只用于修正 TREK Atlas 的显示图层，不修改用户账户、行程记录或地区数据库代码，也不把 Ladakh 等地区的数据库归属迁移到中国。

## 来源和处理过程

- 输入数据：GeoJSON.CN 的“天地图-国家标准矢量地图”数据页；
- 来源页面：<https://geojson.cn/data/file/Tiandi_China>；
- 数据源标注：天地图；
- 本地输入文件元数据：`copyright=Copyright (c) 2025 GeoJSON.CN`，日期 `2025-12-16`；
- 坐标系：CGCS2000 / EPSG:4490；
- 处理脚本：[`deploy/custom-atlas/build_china_boundaries.py`](../deploy/custom-atlas/build_china_boundaries.py)；
- 处理方式：合并中国省级几何，裁掉与中国图层重叠的外部行政区显示几何，再写入 TREK 所需的 admin-0/admin-1 属性结构。

GeoJSON.CN 的资料页列出了来源资料的审图号 `GS(2024) 0650`。该信息用于记录来源，不表示本仓库对处理后的 TREK 图层取得了新的地图审核批准，也不表示本项目获得自然资源主管部门或 GeoJSON.CN 的官方背书。

## 公开使用边界

本声明用于提供来源透明度和软件数据说明，不能替代地图审核批准文件、审图号、备案、测绘资质或平台审核。公开网站、App、社交媒体内容或商业服务上线前，运营者应根据实际用途向有权机关和平台完成适用的地图审核、备案、底图归属和内容安全检查。

不得把“为了通过中国社交媒体审核”写成已经通过审核的证明，也不得伪造、冒用审图号或官方授权。平台是否通过审核由平台和主管机关按实际页面、底图、服务方式及运营主体独立判断。

## 发布文件校验

本版本发布资产的 SHA-256：

```text
admin0.geojson.gz  fb4514e70c4314c3dd15bdb5136a0a29e00dc5031db41f76c8dd3b82caa5c0f3
admin1.geojson.gz  b972a19c8f22fac41f8d8228816515e2daeaf8a91f882148283f0b2f7318d68b
```

发布前请核对下载文件哈希，并把数据来源、更新时间和许可记录保存在 VPS 的部署档案中。数据源或 TREK 版本变化后，应重新生成并重新验证，不要只替换文件名。

