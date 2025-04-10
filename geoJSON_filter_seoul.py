import geopandas as gpd

# 원본 GeoJSON 파일 경로
input_path = "shp_file_to_geojson.geojson"

# 결과 파일 경로
output_path = "seoul_trails.geojson"

# 서울의 산 이름 리스트
seoul_mountains = [
    "개화산", "고덕산", "관악산", "구룡산", "남산", "대모산", "도봉산",
    "매봉산", "봉산", "북악산", "북한산", "불암산", "성산", "수락산", "아차산",
    "안산", "용마산", "우면산", "응봉산", "인왕산", "청계산"
]

# GeoJSON 불러오기
gdf = gpd.read_file(input_path)

# 산 이름이 리스트에 포함된 것만 필터링
filtered_gdf = gdf[gdf['MNTN_NM'].isin(seoul_mountains)]

# 결과 저장
filtered_gdf.to_file(output_path, driver="GeoJSON")

print(f"서울 등산로만 추출 완료 → {output_path}")