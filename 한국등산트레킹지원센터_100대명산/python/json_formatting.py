import os
import json
import random
import math

# 랜덤 hex 색상 생성 함수
def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

# 거리 계산 함수 (하버사인 공식)
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # 지구 반지름 (미터)
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad
    a = math.sin(delta_lat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# 경로 설정
base_dir = os.path.dirname(__file__)
json_path = os.path.join(base_dir, '../mnt_100_convert_json')
convert_path = os.path.join(base_dir, '../mnt_100_convert_json_format')
os.makedirs(convert_path, exist_ok=True)

# 산 이름 폴더 순회
for mountain_folder in os.listdir(json_path):
    mountain_path = os.path.join(json_path, mountain_folder)

    if os.path.isdir(mountain_path):
        for filename in os.listdir(mountain_path):
            if filename.endswith('.json'):
                input_file_path = os.path.join(mountain_path, filename)

                try:
                    with open(input_file_path, 'r', encoding='utf-8') as f:
                        waypoints = json.load(f)

                    sections = []
                    i = 0
                    path_id = 0
                    while i < len(waypoints) - 1:
                        lat1 = waypoints[i]['lat']
                        lon1 = waypoints[i]['lon']
                        lat2 = waypoints[i+1]['lat']
                        lon2 = waypoints[i+1]['lon']

                        length = calculate_distance(lat1, lon1, lat2, lon2)
                        time_minutes = length / 60

                        start_names = [waypoints[i].get('name', f"Point {i}")]

                        # 걸리는 시간이 0분인 경우
                        while time_minutes < 1 and i + 2 < len(waypoints):
                            # 다음다음의 경로와 통합
                            next_lat = waypoints[i+2]['lat']
                            next_lon = waypoints[i+2]['lon']
                            next_length = calculate_distance(lat2, lon2, next_lat, next_lon)
                            next_time = next_length / 60

                            lat2 = next_lat
                            lon2 = next_lon
                            length += next_length
                            time_minutes += next_time
                            i += 1
                            start_names.append(waypoints[i].get('name', f"Point {i}"))

                        section = {
                            "path_id": path_id,
                            "path": [
                                {"lat": lat1, "lng": lon1},
                                {"lat": lat2, "lng": lon2}
                            ],
                            "color": random_color(),
                            "start_name": " / ".join(start_names),
                            "length_meter": round(length,1),
                            "time_minute": math.floor(time_minutes),
                        }
                        sections.append(section)
                        path_id += 1
                        i += 1

                    output_mountain_dir = os.path.join(convert_path, mountain_folder)
                    os.makedirs(output_mountain_dir, exist_ok=True)
                    output_file_path = os.path.join(output_mountain_dir, filename)

                    with open(output_file_path, 'w', encoding='utf-8') as f:
                        json.dump(sections, f, ensure_ascii=False, indent=2)

                    print(f"✅ {mountain_folder}/{filename} 변환 완료")

                except Exception as e:
                    print(f"❌ {mountain_folder}/{filename} 오류 발생: {e}")
