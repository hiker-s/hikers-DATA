import os
import json

# 경로 설정
base_dir = os.path.dirname(__file__)
json_path = os.path.join(base_dir, '../mnt_100_convert_json_format')
convert_path = os.path.join(base_dir, '../mnt_100_convert_json_format_add_min_ele')
os.makedirs(convert_path, exist_ok=True)

# 최소 고도 계산
def extract_min_ele(track_data):
    elevations = []
    for segment in track_data:
        for point in segment.get("path", []):
            ele = point.get("ele")
            if isinstance(ele, (int, float)):
                elevations.append(ele)
    return min(elevations) if elevations else 0

# 전체 폴더 탐색
for mountain_folder in os.listdir(json_path):
    mountain_dir = os.path.join(json_path, mountain_folder)

    if not os.path.isdir(mountain_dir):
        continue

    # 저장 폴더 생성
    save_dir = os.path.join(convert_path, mountain_folder)
    os.makedirs(save_dir, exist_ok=True)

    for file_name in os.listdir(mountain_dir):
        if not file_name.endswith('.json'):
            continue

        file_path = os.path.join(mountain_dir, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        track_data = data.get("track", [])
        min_ele = extract_min_ele(track_data)
        data["min_ele"] = min_ele

        # 저장
        save_path = os.path.join(save_dir, file_name)
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

print("min_ele 추가 완료")