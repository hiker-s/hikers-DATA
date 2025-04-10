import os
import folium
import json
import hashlib

# GeoJSON 파일 경로
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
geojson_path = os.path.join(base_dir, "result_json", "shp_wgs84_seoul_trails.geojson")

# GeoJSON 불러오기
with open(geojson_path, encoding='utf-8') as f:
    geojson_data = json.load(f)

# 중심 좌표 설정
first_feature = geojson_data["features"][0]
first_coords = first_feature["geometry"]["coordinates"][0][0]
center_lat = first_coords[1]
center_lon = first_coords[0]

# folium 지도 생성
m = folium.Map(location=[center_lat, center_lon], zoom_start=13)

# PMNTN_SN 값을 기반으로 색상 생성
def get_color_from_sn(sn):
    sn_str = str(sn)
    hash_object = hashlib.md5(sn_str.encode())
    return "#" + hash_object.hexdigest()[:6]

# feature별 지도에 추가
for feature in geojson_data["features"]:
    props = feature["properties"]
    sn = props.get("PMNTN_SN")

    folium.GeoJson(
        feature,
        style_function=lambda f, sn=sn: {
            "color": get_color_from_sn(sn),
            "weight": 4,
            "opacity": 0.9,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["MNTN_NM", "PMNTN_NM", "PMNTN_DFFL", "PMNTN_LT"],
            aliases=["산 이름", "구간 이름", "난이도", "거리 (km)"],
            localize=True
        )
    ).add_to(m)

# 저장 경로
output_path = os.path.join(base_dir, "result_html", "map_colored_by_sn.html")
m.save(output_path)
print(f"✅ 저장 완료: {output_path}")