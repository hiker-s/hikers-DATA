import os
import json
import random

# 랜덤 hex 색상 생성 함수
def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

# 경로 설정
base_dir = os.path.dirname(__file__)
json_path = os.path.join(base_dir, '../mnt_100_convert_json')
convert_path = os.path.join(base_dir, '../mnt_100_convert_json_format')
os.makedirs(convert_path, exist_ok=True)

# 산 이름 폴더 순회
for mountain_folder in os.listdir(json_path):
    mountain_path = os.path.join(json_path, mountain_folder)

    # 폴더인 경우만 처리
    if os.path.isdir(mountain_path):
        for filename in os.listdir(mountain_path):
            if filename.endswith('.json'):
                input_file_path = os.path.join(mountain_path, filename)

                try:
                    # 원본 JSON 로드
                    with open(input_file_path, 'r', encoding='utf-8') as f:
                        waypoints = json.load(f)

                    # 두 점씩 연결해서 section 생성
                    sections = []
                    for i in range(len(waypoints) - 1):
                        section = {
                            "path": [
                                {"lat": waypoints[i]['lat'], "lng": waypoints[i]['lon']},
                                {"lat": waypoints[i+1]['lat'], "lng": waypoints[i+1]['lon']}
                            ],
                            "color": random_color()
                        }
                        sections.append(section)

                    # 저장 경로 구성
                    output_mountain_dir = os.path.join(convert_path, mountain_folder)
                    os.makedirs(output_mountain_dir, exist_ok=True)
                    output_file_path = os.path.join(output_mountain_dir, filename)

                    # 변환된 JSON 저장
                    with open(output_file_path, 'w', encoding='utf-8') as f:
                        json.dump(sections, f, ensure_ascii=False, indent=2)

                    print(f"✅ {mountain_folder}/{filename} 변환 완료")

                except Exception as e:
                    print(f"❌ {mountain_folder}/{filename} 오류 발생: {e}")