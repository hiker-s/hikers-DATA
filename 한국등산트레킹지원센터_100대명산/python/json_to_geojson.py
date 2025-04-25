import os
import json

# 경로 설정
base_dir = os.path.dirname(__file__)
mnt_100_path = os.path.join(base_dir, '../mnt_100_convert_json')
convert_path = os.path.join(base_dir, '../mnt_100_convert_geojson')
os.makedirs(convert_path, exist_ok=True)

# 각 산 폴더 반복
for mountain_name in os.listdir(mnt_100_path):
    mountain_folder = os.path.join(mnt_100_path, mountain_name)
    if not os.path.isdir(mountain_folder):
        continue

    output_mountain_folder = os.path.join(convert_path, mountain_name)
    os.makedirs(output_mountain_folder, exist_ok=True)

    for filename in os.listdir(mountain_folder):
        if not filename.endswith(".json"):
            continue

        file_path = os.path.join(mountain_folder, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print(f"⚠️ JSON 파싱 오류: {file_path}")
                continue

        # 좌표 추출 (lon, lat)
        coordinates = [[point["lon"], point["lat"]] for point in data]

        # GeoJSON 구조 생성
        geojson = {
            "type": "FeatureCollection",
            "name": mountain_name,
            "crs": {
                "type": "name",
                "properties": {
                    "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
                }
            },
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        
                    },
                    "geometry": {
                        "type": "MultiLineString",
                        "coordinates": [coordinates]
                    }
                }
            ]
        }

        # 저장
        output_filename = os.path.splitext(filename)[0] + '.geojson'
        output_path = os.path.join(output_mountain_folder, output_filename)
        with open(output_path, 'w', encoding='utf-8') as out_f:
            json.dump(geojson, out_f, ensure_ascii=False, indent=2)

        print(f"변환 완료: {output_filename}")