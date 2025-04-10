import geopandas as gpd
import json
import os
from datetime import datetime

# 현재 파일 기준 geojson_wgs84 폴더 경로 얻기
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# 생성시간 기준 결과 폴더 경로 설정
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
result_dir = os.path.join(base_dir, f"result_json")
os.makedirs(result_dir, exist_ok=True)

# 입력/출력 경로
input_path = os.path.join(base_dir, "shp_wgs84.geojson")
final_output_path = os.path.join(result_dir, "shp_wgs84_seoul_trails.geojson")

# 1. 제거할 컬럼 목록
columns_to_remove = [
    "PMNTN_MTRQ", "PMNTN_CNRL", "PMNTN_CLS", 
    "PMNTN_RISK", "PMNTN_RECO", "DATA_STDR", "PMNTN_MAIN"
]

# 2. GeoJSON 불러오기 및 컬럼 제거
with open(input_path, "r", encoding="utf-8") as f:
    geojson_data = json.load(f)

for feature in geojson_data["features"]:
    for column in columns_to_remove:
        feature["properties"].pop(column, None)

# 3. GeoDataFrame으로 변환
gdf = gpd.GeoDataFrame.from_features(geojson_data["features"])

# 4. 서울 주요 산 필터링
seoul_mountains = [
    "개화산", "고덕산", "관악산", "구룡산", "남산", "대모산", "도봉산",
    "매봉산", "북악산", "북한산", "불암산", "수락산", "아차산",
    "안산", "용마산", "우면산", "응봉산", "인왕산", "청계산"
]
gdf = gdf[gdf["MNTN_NM"].isin(seoul_mountains)]

# 5. 위경도 필터링 함수
SEOUL_LAT_MIN, SEOUL_LAT_MAX = 37.4133, 37.7151
SEOUL_LON_MIN, SEOUL_LON_MAX = 126.7341, 127.2693

def is_within_seoul(geometry):
    if geometry.geom_type == "MultiLineString":
        for line in geometry.geoms:
            for lon, lat in line.coords:
                if (SEOUL_LAT_MIN <= lat <= SEOUL_LAT_MAX) and (SEOUL_LON_MIN <= lon <= SEOUL_LON_MAX):
                    return True
    elif geometry.geom_type == "LineString":
        for lon, lat in geometry.coords:
            if (SEOUL_LAT_MIN <= lat <= SEOUL_LAT_MAX) and (SEOUL_LON_MIN <= lon <= SEOUL_LON_MAX):
                return True
    return False

# 6. 서울 범위 내 데이터만 필터링
gdf = gdf[gdf.geometry.apply(is_within_seoul)]

# 7. 최종 결과 저장
gdf.to_file(final_output_path, driver="GeoJSON")

print(f"✅ 저장 완료: {final_output_path}")