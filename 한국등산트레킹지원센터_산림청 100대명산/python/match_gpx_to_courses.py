import os
import json
import xml.etree.ElementTree as ET

# 상위 폴더의 JSON 파일 경로
base_dir = os.path.dirname(__file__)
json_path = os.path.join(base_dir, '../mnt_100_info_course_start_end.json')
mnt_folder_path = os.path.join(base_dir, '../mnt_100')  # 산 폴더들이 있는 경로
result_path = os.path.join(base_dir, '../matching_gpx_by_mountain.json')  # 결과 저장 경로

# JSON 데이터 로드
with open(json_path, 'r', encoding='utf-8') as f:
    mountains = json.load(f)

# GPX에서 첫 번째 wpt name 추출 함수
def get_first_wpt_name(gpx_file):
    try:
        tree = ET.parse(gpx_file)
        root = tree.getroot()

        ns = {'default': 'http://www.topografix.com/GPX/1/1'}
        wpt = root.find('default:wpt', ns)
        if wpt is not None:
            name = wpt.find('default:name', ns)
            if name is not None and name.text:
                return name.text.strip()
    except ET.ParseError:
        pass
    return None

# 결과를 저장할 리스트
result = []

# 산 폴더 순회
for mountain in mountains:
    mnt_name = mountain.get('mnt_name')
    course_starts = []

    # 각 course에서 start만 수집
    for i in range(1, 6):
        course_key = f'mnt_course_{i}'
        if course_key in mountain and isinstance(mountain[course_key], dict):
            start = mountain[course_key].get('start')
            if start:
                course_starts.append(start.strip())

    matched_gpx = []

    mountain_dir = os.path.join(mnt_folder_path, mnt_name)
    if os.path.isdir(mountain_dir):
        for file in os.listdir(mountain_dir):
            if file.endswith('.gpx'):
                gpx_path = os.path.join(mountain_dir, file)
                first_name = get_first_wpt_name(gpx_path)
                if first_name and any(first_name in start for start in course_starts):
                    matched_gpx.append(file)

    result.append({
        "mnt_name": mnt_name,
        "matched_gpx_files": matched_gpx
    })

# 결과 저장
with open(result_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("매칭된 gpx 파일이 matching_gpx_by_mountain.json에 저장되었습니다.")