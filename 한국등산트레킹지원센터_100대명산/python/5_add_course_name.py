import os
import json
from collections import OrderedDict  

# 경로 설정
base_dir = os.path.dirname(__file__)
json_path = os.path.join(base_dir, '../mnt_100_result/mnt_100_convert_json_format_add_level')
convert_path = os.path.join(base_dir, '../mnt_100_result/mnt_100_convert_json_format_add_name')
os.makedirs(convert_path, exist_ok=True)

name_low = [
    "산들산책 코스",     # 부드러운 바람과 함께 걷는 느낌
    "초록오름 코스",     # 초록빛 산길을 따라
    "가벼운산길 코스",   # 부담 없이 산을 오르는 느낌
    "햇살등산 코스"      # 산길과 햇살이 함께하는
]

name_mid = [
    "중턱오름 코스",     # 산 중턱을 향해 오르는
    "꾸준오름 코스",     # 지속적으로 오르는 산길
    "산중길 코스",       # 산 속 깊은 길
    "탄력등산 코스"      # 탄탄하게 오르는 느낌
]

name_high = [
    "가파른산길 코스",   # 경사도 강조
    "거친산길 코스",     # 도전적인 험한 길
    "극한오름 코스",     # 극한의 오름
    "상급등산 코스"      # 상급자에게 적합
]

# 전체 폴더 탐색
for mountain_folder in os.listdir(json_path):
    mountain_dir = os.path.join(json_path, mountain_folder)

    if not os.path.isdir(mountain_dir):
        continue

    # 각 난이도별 인덱스 초기화
    idx_low, idx_mid, idx_high = 0, 0, 0

    # 저장 폴더 생성
    save_dir = os.path.join(convert_path, mountain_folder)
    os.makedirs(save_dir, exist_ok=True)

    for file_name in os.listdir(mountain_dir):
        if not file_name.endswith('.json'):
            continue

        file_path = os.path.join(mountain_dir, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # level에 따라 코스 이름 설정
        level = data.get("level", "")
        if level == "상":
            data["course_name"] = name_high[idx_high % len(name_high)]
            idx_high += 1
        elif level == "중":
            data["course_name"] = name_mid[idx_mid % len(name_mid)]
            idx_mid += 1
        else:
            data["course_name"] = name_low[idx_low % len(name_low)]
            idx_low += 1

        # key 순서바꾸기
        reordered_data = OrderedDict()
        reordered_data["mnt_id"] = data.get("mnt_id")
        reordered_data["mnt_name"] = data.get("mnt_name")
        reordered_data["course_id"] = data.get("course_id")
        reordered_data["max_ele"] = data.get("max_ele")
        reordered_data["total_length_km"] = data.get("total_length_km")
        reordered_data["total_time"] = data.get("total_time")
        reordered_data["start_name"] = data.get("start_name")
        reordered_data["end_name"] = data.get("end_name")
        reordered_data["level"] = data.get("level")
        reordered_data["course_name"] = data.get("course_name") 
        reordered_data["min_ele"] = data.get("min_ele")
        reordered_data["track"] = data.get("track")

        # 누락된 키가 있다면 추가
        for key in data:
            if key not in reordered_data:
                reordered_data[key] = data[key]

        # 저장
        save_path = os.path.join(save_dir, file_name)
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(reordered_data, f, ensure_ascii=False, indent=2)

print("코스 이름 추가 및 순서 재정렬 완료")