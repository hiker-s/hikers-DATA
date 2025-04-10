import geopandas as gpd
import json


# 원본 GeoJSON 파일 경로
input_path = "shp_file_to_geojson.geojson"
filter_cols_path = "shp_file_to_geojson_filter_cols.geojson" # 불필요한 행 제거한 json
output_path = "seoul_trails.geojson"



# 불필요한 열 리스트
columns_to_remove = [
    "PMNTN_MTRQ", "PMNTN_CNRL", "PMNTN_CLS", 
    "PMNTN_RISK", "PMNTN_RECO", "DATA_STDR", "PMNTN_MAIN"
]

# GeoJSON 파일 로딩
with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 각 feature의 properties에서 불필요한 열 제거
for feature in data["features"]:
    for column in columns_to_remove:
        feature["properties"].pop(column, None)  # 열이 없을 경우도 대비해 None 추가

# 결과 저장
with open(filter_cols_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)





# 서울 산 리스트
seoul_mountains = [
    "개화산", "고덕산", "관악산", "구룡산", "남산", "대모산", "도봉산",
    "매봉산", "북악산", "북한산", "불암산", "수락산", "아차산",
    "안산", "용마산", "우면산", "응봉산", "인왕산", "청계산"
]

# GeoJSON 불러오기
gdf = gpd.read_file(filter_cols_path)

# 서울 산 필터 + PMNTN_MAIN null 값이 없는 것만 추리기
filtered_gdf = gdf[
    (gdf["MNTN_NM"].isin(seoul_mountains)) &
    (gdf["PMNTN_NM"].notnull())
]

# 결과 저장
filtered_gdf.to_file(output_path, driver="GeoJSON")

print(f"필터링 완료 : {output_path}")