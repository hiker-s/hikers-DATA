import geopandas as gpd
import json

# 경로 설정
input_path = "shp_wgs84.geojson"
intermediate_path = "shp_filtered_columns.geojson" # 불필요한 col 제거
filtered_by_mountain_path = "shp_filtered_mountains.geojson" # 서울산 이름으로 1차 필터링
filtered_by_location_path = "shp_filtered_seoul_location.geojson" # 서울 위경도 사이로 2차 필터링
final_output_path = "shp_wgs84_seoul_trails.geojson"

# 1. 제거할 컬럼 목록
columns_to_remove = [
    "PMNTN_MTRQ", "PMNTN_CNRL", "PMNTN_CLS", 
    "PMNTN_RISK", "PMNTN_RECO", "DATA_STDR", "PMNTN_MAIN"
]

# 2. GeoJSON 불러와 불필요한 컬럼 제거
with open(input_path, "r", encoding="utf-8") as f:
    geojson_data = json.load(f)

for feature in geojson_data["features"]:
    for column in columns_to_remove:
        feature["properties"].pop(column, None)

# 제거 후 중간 저장
with open(intermediate_path, "w", encoding="utf-8") as f:
    json.dump(geojson_data, f, ensure_ascii=False, indent=2)

# 3. 서울 주요 산 이름 목록 필터링
seoul_mountains = [
    "개화산", "고덕산", "관악산", "구룡산", "남산", "대모산", "도봉산",
    "매봉산", "북악산", "북한산", "불암산", "수락산", "아차산",
    "안산", "용마산", "우면산", "응봉산", "인왕산", "청계산"
]

gdf = gpd.read_file(intermediate_path)
filtered_gdf = gdf[
    (gdf["MNTN_NM"].isin(seoul_mountains)) &
    (gdf["PMNTN_NM"].notnull())
]
filtered_gdf.to_file(filtered_by_mountain_path, driver="GeoJSON")

# 4. 위경도 범위로 서울 안인지 확인
SEOUL_LAT_MIN, SEOUL_LAT_MAX = 37.4133, 37.7151
SEOUL_LON_MIN, SEOUL_LON_MAX = 126.7341, 127.2693

def is_within_seoul(geometry):
    if geometry.geom_type == "MultiLineString":
        for line in geometry.geoms:  # 수정된 부분!
            for lon, lat in line.coords:
                if (SEOUL_LAT_MIN <= lat <= SEOUL_LAT_MAX) and (SEOUL_LON_MIN <= lon <= SEOUL_LON_MAX):
                    return True
    elif geometry.geom_type == "LineString":
        for lon, lat in geometry.coords:
            if (SEOUL_LAT_MIN <= lat <= SEOUL_LAT_MAX) and (SEOUL_LON_MIN <= lon <= SEOUL_LON_MAX):
                return True
    return False

# 5. 위경도 필터링 적용
filtered_gdf = gpd.read_file(filtered_by_mountain_path)
filtered_gdf = filtered_gdf[filtered_gdf.geometry.apply(is_within_seoul)]
filtered_gdf.to_file(final_output_path, driver="GeoJSON")

print(f"✅ 필터링 완료: {final_output_path}")