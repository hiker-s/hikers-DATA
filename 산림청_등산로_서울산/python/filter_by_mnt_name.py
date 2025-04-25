import json
import os
from collections import defaultdict

# 1. 원본 JSON 파일 열기
with open('../원본/mnt_seoul.geojson', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 2. 산 이름별로 feature 분류
mountain_dict = defaultdict(list)

for feature in data['features']:
    mountain_name = feature['properties']['MNTN_NM']
    mountain_dict[mountain_name].append(feature)

# 3. 산 이름별로 폴더 생성 후 파일 저장
output_base_dir = '../원본을_산별로_저장'
os.makedirs(output_base_dir, exist_ok=True)

for mountain_name, features in mountain_dict.items():
    folder_name = os.path.join(output_base_dir, mountain_name)
    os.makedirs(folder_name, exist_ok=True)

    output_data = {
        "type": "FeatureCollection",
        "name": mountain_name,
        "crs": data["crs"],
        "features": features
    }

    # 산 이름에 특수문자가 있을 수 있으니 파일 이름은 안전하게
    filename = f"{mountain_name}.geojson".replace("/", "_")
    output_path = os.path.join(folder_name, filename)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

print("산 이름별 GeoJSON 저장 완료")