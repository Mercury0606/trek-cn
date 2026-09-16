#!/usr/bin/env python3
"""Replace TREK's China boundaries with Tiandi standard-vector geometries.

The source file is the Tiandi-derived GeoJSON downloaded from geojson.cn.  The
script makes that China geometry authoritative in both admin-0 and admin-1,
while preserving the original country and region identifiers outside it.
"""

from __future__ import annotations

import gzip
import json
from pathlib import Path

from shapely.geometry import GeometryCollection, MultiPolygon, Polygon, mapping, shape
from shapely.ops import unary_union
from shapely.prepared import prep
from shapely.validation import make_valid


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "tiandi" / "100000.json"
ORIGINAL = ROOT / "original"
OUTPUT = ROOT


def read_gzip(path: Path) -> dict:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        return json.load(handle)


def write_gzip(path: Path, value: dict) -> None:
    payload = json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    with path.open("wb") as raw:
        with gzip.GzipFile(fileobj=raw, mode="wb", compresslevel=9, mtime=0) as handle:
            handle.write(payload)


def is_province(feature: dict) -> bool:
    code = feature.get("properties", {}).get("code")
    return isinstance(code, str) and len(code) == 6 and code.isdigit()


def polygonal_or_empty(geometry):
    """Keep only polygonal pieces after clipping overlapping country features."""
    geometry = make_valid(geometry)
    if isinstance(geometry, (Polygon, MultiPolygon)):
        return geometry
    if isinstance(geometry, GeometryCollection):
        parts = [
            part
            for part in geometry.geoms
            if isinstance(part, (Polygon, MultiPolygon)) and not part.is_empty
        ]
        return unary_union(parts) if parts else GeometryCollection()
    return GeometryCollection()


def main() -> None:
    tiandi = json.loads(SOURCE.read_text(encoding="utf-8"))
    provinces = [feature for feature in tiandi["features"] if is_province(feature)]
    if len(provinces) != 34:
        raise RuntimeError(f"Expected 34 province-level features, got {len(provinces)}")

    province_geometries = [shape(feature["geometry"]) for feature in provinces]
    china_geometry = unary_union(province_geometries)
    if china_geometry.is_empty or not china_geometry.is_valid:
        raise RuntimeError("The merged China geometry is empty or invalid")
    china_prepared = prep(china_geometry)

    admin0 = read_gzip(ORIGINAL / "admin0.geojson.gz")
    china_count = 0
    clipped_country_codes = []
    admin0_features = []
    china_feature = None
    for feature in admin0["features"]:
        props = feature.get("properties", {})
        if props.get("ADM0_A3") == "CHN" or props.get("ISO_A2") == "CN":
            china_count += 1
            china_feature = {
                "type": "Feature",
                "properties": {
                    "ISO_A2": "CN",
                    "ADM0_A3": "CHN",
                    "NAME": "China",
                    "ADMIN": "China",
                },
                "geometry": mapping(china_geometry),
            }
        else:
            country_geometry = make_valid(shape(feature["geometry"]))
            if country_geometry.intersects(china_geometry):
                clipped = polygonal_or_empty(country_geometry.difference(china_geometry))
                replaced = dict(feature)
                replaced["geometry"] = mapping(clipped)
                admin0_features.append(replaced)
                clipped_country_codes.append(str(props.get("ISO_A2") or "?"))
            else:
                admin0_features.append(feature)
    if china_count != 1:
        raise RuntimeError(f"Expected one China admin-0 feature, got {china_count}")

    # Leaflet's canvas renderer paints later features on top.  The Tiandi China
    # geometry overlaps several disputed polygons in TREK's original global
    # dataset, so append China last to make this configured GeoJSON authoritative
    # for the visible country outline without changing any region attribution.
    admin0_features.append(china_feature)

    admin1 = read_gzip(ORIGINAL / "admin1.geojson.gz")
    admin1_features = []
    clipped_region_codes = []
    removed_region_codes = []
    for feature in admin1["features"]:
        props = feature.get("properties", {})
        country_code = str(props.get("iso_a2") or "").upper()
        if country_code == "CN":
            continue

        # Taiwan's detailed regions remain available for TREK's existing TW-*
        # visit records. Their selected colour is normalized in the Atlas UI.
        if country_code == "TW":
            admin1_features.append(feature)
            continue

        region_geometry = make_valid(shape(feature["geometry"]))
        if not china_prepared.intersects(region_geometry):
            admin1_features.append(feature)
            continue

        clipped = polygonal_or_empty(region_geometry.difference(china_geometry))
        removed_area = region_geometry.area - clipped.area
        if removed_area <= 1e-12:
            admin1_features.append(feature)
            continue

        region_code = str(props.get("iso_3166_2") or "?")
        if clipped.is_empty:
            removed_region_codes.append(region_code)
            continue

        replaced = dict(feature)
        replaced["geometry"] = mapping(clipped)
        admin1_features.append(replaced)
        clipped_region_codes.append(region_code)

    for feature in provinces:
        props = feature["properties"]
        code = props["code"]
        name = props["name"]
        admin1_features.append(
            {
                "type": "Feature",
                "properties": {
                    "iso_a2": "CN",
                    "iso_3166_2": f"CN-{code}",
                    "name": name,
                    "name_en": name,
                    "admin": "China",
                },
                "geometry": feature["geometry"],
            }
        )

    write_gzip(
        OUTPUT / "admin0.geojson.gz",
        {"type": "FeatureCollection", "features": admin0_features},
    )
    write_gzip(
        OUTPUT / "admin1.geojson.gz",
        {"type": "FeatureCollection", "features": admin1_features},
    )

    print(f"admin0: {len(admin0_features)} features; replaced {china_count} China feature")
    print(f"admin0: clipped overlaps from {','.join(clipped_country_codes)}")
    print(f"admin1: {len(admin1_features)} features; replaced {len(provinces)} China regions")
    print(f"admin1: clipped overlaps from {','.join(clipped_region_codes)}")
    print(f"admin1: removed fully covered regions {','.join(removed_region_codes) or 'none'}")
    print(f"China geometry type: {china_geometry.geom_type}")


if __name__ == "__main__":
    main()
