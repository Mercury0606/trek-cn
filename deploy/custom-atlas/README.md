# TREK Atlas 中国边界覆盖

这组文件保留 TREK 原有的全球边界，只替换中国的国家轮廓和省级行政区轮廓。

来源：

- `tiandi/100000.json`：来自 `geojson.cn` 提供的“天地图-国家标准矢量地图”转换数据，数据源标注为天地图；坐标系为 CGCS2000（EPSG:4490）。
- `original/`：从本地 `mauriceboe/trek:4.2.1` 容器备份的原始 geoBoundaries 文件。
- `build_china_boundaries.py`：将中国 34 个省级单元合并为国家轮廓，并合并回 TREK 全球文件。

Ladakh 保持 TREK 原有的 `IN-LA` 地区代码和访问记录，不做归属迁移；其显示几何会裁掉与中国 GeoJSON 重叠的部分。

中国国家级 Feature 被放在全球 GeoJSON 的最后绘制，避免印度、巴基斯坦、台湾等原始重叠多边形覆盖中国 GeoJSON；这只调整显示层级，不修改这些地区的数据库归属。

构建时会从其他国家的 admin-0 显示多边形，以及非中国、非台湾的 admin-1 地区多边形中，裁掉与中国 GeoJSON 重叠的部分，避免 `IN-AR`、`IN-LA` 等省级图形再次覆盖中国。台湾 admin-1 保留以支持现有 `TW-*` 访问记录；所有数据库归属和用户记录均不改变。

`../custom-frontend/useAtlas-Cdw1eKU9.js` 给 Atlas 边界请求增加本地缓存版本号，避免浏览器继续使用旧的 24 小时接口缓存；同时让台湾已访问省级区域复用中国的选中颜色，数据库中的 `TW-*` 地区代码保持不变。

`../custom-frontend/MAtlas-Dl6uc9sE.js` 将台湾地区操作弹窗的国家文字和旗帜显示为中国；保存和查询时仍使用原有 `TW-*` 代码，以兼容已有访问记录。

`../custom-frontend/VectorBasemap-B_2s89GS.js` 保留 OpenFreeMap Positron 底图，但在 Atlas 隐藏其 `boundary_disputed` 争议边界图层，避免该底图的虚线覆盖自定义中国 GeoJSON。

`../custom-frontend/sw.js` 为上述前端覆盖设置本地缓存版本，保证浏览器刷新后载入新文件。

这不是自然资源部直接发布的 GeoJSON，也不等同于地图审核批准。公开发布地图前，应使用自然资源部标准地图服务并按规定进行审核。
