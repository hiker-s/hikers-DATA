import os
import json
import random
import math

# 경로 설정
base_dir = os.path.dirname(__file__)
json_path = os.path.join(base_dir, '../mnt_100_result/mnt_100_convert_json_filter_duplication')
convert_path = os.path.join(base_dir, '../mnt_100_result/mnt_100_convert_json_format')
os.makedirs(convert_path, exist_ok=True)

# 정제 제외할 산
skip_mnt = ["가리산", "금산", "대암산", "축령산", "덕숭산", "민주지산"]

# 걸음 속도 4.8 km/h => 80 m/min
walking_speed_m_per_min = 80

def random_color():
    while True:
        hex_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        if r < 200 and g < 200 and b < 200:
            return hex_color

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad
    a = math.sin(delta_lat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def merge_short_segments(i, waypoints, lat2, lon2, length, time_minutes, start_names):
    while time_minutes < 1 and i + 2 < len(waypoints):
        next_name = waypoints[i + 2].get("name", "")
        if "갈림길" in next_name:
            break

        next_lat = waypoints[i + 2]['lat']
        next_lon = waypoints[i + 2]['lon']
        next_length = calculate_distance(lat2, lon2, next_lat, next_lon)
        next_time = next_length / 60

        lat2 = next_lat
        lon2 = next_lon
        length += next_length
        time_minutes += next_time
        i += 1
        start_names.append(waypoints[i].get('name', f"Point {i}"))

    return i, lat2, lon2, length, time_minutes, start_names

def create_section(path_id, lat1, lon1, ele1, lat2, lon2, ele2, start_names, end_name, length, time_minutes):
    return {
        "path_id": path_id,
        "path": [
            {"lat": lat1, "lng": lon1, "ele": ele1},
            {"lat": lat2, "lng": lon2, "ele": ele2}
        ],
        "color": random_color(),
        "start_name": " / ".join(start_names),
        "end_name": end_name,
        "length_meter": round(length, 1),
        "time_minute": math.floor(time_minutes)
    }

# 산 폴더 정렬 후 ID 부여
mountain_folders = sorted(os.listdir(json_path))
course_id = 0  # 전체 course 고유 ID

for mnt_id, mountain_folder in enumerate(mountain_folders, start=1): 
    mountain_path = os.path.join(json_path, mountain_folder)

    if os.path.isdir(mountain_path):
        for filename in os.listdir(mountain_path):
            if filename.endswith('.json'):
                input_file_path = os.path.join(mountain_path, filename)

                try:
                    with open(input_file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    if "track" not in data or not isinstance(data["track"], list):
                        print(f"⚠️ {mountain_folder}/{filename} → 'track' 누락 또는 형식 오류")
                        continue

                    waypoints = data["track"]

                    sections = []
                    i = 0
                    path_id = 0

                    total_length = 0  # 총 길이 누적 변수

                    while i < len(waypoints) - 1:
                        lat1 = waypoints[i]['lat']
                        lon1 = waypoints[i]['lon']
                        ele1 = waypoints[i].get('ele', 0)

                        lat2 = waypoints[i+1]['lat']
                        lon2 = waypoints[i+1]['lon']
                        ele2 = waypoints[i+1].get('ele', 0)

                        length = calculate_distance(lat1, lon1, lat2, lon2)
                        time_minutes = length / walking_speed_m_per_min
                        start_names = [waypoints[i].get('name', f"Point {i}")]

                        if mountain_folder not in skip_mnt:
                            i, lat2, lon2, length, time_minutes, start_names = merge_short_segments(
                                i, waypoints, lat2, lon2, length, time_minutes, start_names
                            )
                            ele2 = waypoints[i+1].get('ele', 0)
                        else:
                            print(f"{mountain_folder} 제외")

                        total_length += length

                        end_name = waypoints[i+1].get('name', f"Point {i+1}")

                        section = create_section(path_id, lat1, lon1, ele1, lat2, lon2, ele2, start_names, end_name, length, time_minutes)

                        sections.append(section)
                        path_id += 1
                        i += 1

                    output_mountain_dir = os.path.join(convert_path, mountain_folder)
                    os.makedirs(output_mountain_dir, exist_ok=True)
                    output_file_path = os.path.join(output_mountain_dir, filename)

                    # 걸리는 시간 계산 (단위: 분)
                    total_time_minutes = total_length / walking_speed_m_per_min

                    # 시간과 분으로 나누기
                    hours = int(total_time_minutes // 60)
                    minutes = int(total_time_minutes % 60)

                    # 시간 형식 설정 (minutes가 0일 경우 '시간'만 포함)
                    if minutes == 0:
                        total_time_str = f"{hours}시간"
                    else:
                        total_time_str = f"{hours}시간 {minutes}분"

                    

                    # 최종 JSON 데이터 구성
                    output_data = {
                        "mnt_id": mnt_id,
                        "mnt_name": mountain_folder,
                        "course_id": course_id,
                        "max_ele": data["max_ele"],
                        "total_length_km": f"{round(total_length / 1000, 1)}km",
                        "total_time": total_time_str,
                        "start_name": waypoints[0].get('name'), 
                        "end_name": waypoints[-1].get('name'),
                        "level" : "중",
                        "track": sections
                    }

                    course_id += 1

                    with open(output_file_path, 'w', encoding='utf-8') as f:
                        json.dump(output_data, f, ensure_ascii=False, indent=2)

                except Exception as e:
                    print(f"❌ {mountain_folder}/{filename} 오류 발생: {e}")