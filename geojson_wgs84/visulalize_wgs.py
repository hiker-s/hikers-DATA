import folium
import json

# GeoJSON 파일 불러오기
with open('shp_wgs84_seoul_trails.geojson', encoding='utf-8') as f:
    geojson_data = json.load(f)

# 중심 좌표 설정 (첫 번째 Feature의 첫 번째 좌표)
first_feature = geojson_data["features"][0]
first_coords = first_feature["geometry"]["coordinates"][0][0]  # MultiLineString 구조

center_lat = first_coords[1]
center_lon = first_coords[0]

# folium 지도 생성
m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

# GeoJSON 레이어 추가
folium.GeoJson(
    geojson_data,
    name="서울 등산로",
    tooltip=folium.GeoJsonTooltip(
        fields=["MNTN_NM", "PMNTN_NM", "PMNTN_DFFL", "PMNTN_LT"],
        aliases=["산 이름", "구간 이름", "난이도", "거리 (km)"],
        localize=True
    )
).add_to(m)

# 지도 저장
m.save("seoul_trails_map.html")