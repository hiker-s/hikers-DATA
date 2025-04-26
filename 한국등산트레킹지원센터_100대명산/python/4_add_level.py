import os
import json
import re

# 경로 설정
base_dir = os.path.dirname(__file__)
json_path = os.path.join(base_dir, '../mnt_100_result/mnt_100_convert_json_format_add_min_ele')
convert_path = os.path.join(base_dir, '../mnt_100_result/mnt_100_convert_json_format_add_level')
os.makedirs(convert_path, exist_ok=True)

# 미터로 변환
def parse_distance(distance_str):
    try:
        return float(re.sub(r'[^\d.]', '', distance_str)) * 1000  # meters
    except:
        return 0

# 분으로 변환
def parse_time(time_str):
    h = re.search(r'(\d+)시간', time_str)
    m = re.search(r'(\d+)분', time_str)
    hour = int(h.group(1)) if h else 0
    minute = int(m.group(1)) if m else 0
    return hour * 60 + minute

def calculate_difficulty_by_ele(max_ele, min_ele, distance_m):
    # 경사도 기반
    slope_percent = ((max_ele - min_ele) / distance_m) * 100
    point = distance_m * slope_percent

    if point >= 64001:
        return "상"
    elif point >= 20001:
        return "중"
    else:
        return "하"
    
def calculate_difficulty_by_time(time_min):
    # 등산 시간 기반
    if time_min >= 240:
        return "상"
    elif time_min >= 120:
        return "중"
    else:
        return "하"
    
def to_score(level: str) -> int:
    return {"하": 1, "중": 2, "상": 3}.get(level, 1)

def calculate_final_difficulty(ele_level, time_level):
    ele_score = to_score(ele_level)
    time_score = to_score(time_level)

    # 경사도에 조금 더 가중치 부여
    weighted_score = ele_score * 1.7 + time_score * 1.0

    if weighted_score < 4:
        return "하"
    elif weighted_score < 6:
        return "중"
    else:
        return "상"

# 전체 폴더 탐색
for mountain_folder in os.listdir(json_path):
    mountain_dir = os.path.join(json_path, mountain_folder)

    if not os.path.isdir(mountain_dir):
        continue

    # 저장 폴더도 생성
    save_dir = os.path.join(convert_path, mountain_folder)
    os.makedirs(save_dir, exist_ok=True)

    for file_name in os.listdir(mountain_dir):
        if not file_name.endswith('.json'):
            continue

        file_path = os.path.join(mountain_dir, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        max_ele = data.get("max_ele")
        min_ele = data.get("min_ele")
        distance_str = data.get("total_length_km")
        time_str = data.get("total_time")

        distance_m = parse_distance(distance_str)
        time_min = parse_time(time_str)
        level = calculate_final_difficulty(
            calculate_difficulty_by_ele(max_ele, min_ele, distance_m), 
            calculate_difficulty_by_time(time_min)
            )

        data["level"] = level

        # 저장
        save_path = os.path.join(save_dir, file_name)
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

print("난이도 추가 완료")