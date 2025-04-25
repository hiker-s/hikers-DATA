# mnt_100_convert_json 에서
# 이름이 중복되어 연속으로 나오는 객체가 있으면
# 앞 객체만 남기고 뒷 객체 제거

import os
import json

# 경로 설정
base_dir = os.path.dirname(__file__)
json_path = os.path.join(base_dir, '../mnt_100_convert_json_clean')
convert_path = os.path.join(base_dir, '../mnt_100_convert_json_filter_duplication')
os.makedirs(convert_path, exist_ok=True)

# 연속된 같은 이름의 객체 제거 함수
def remove_duplicates(json_data):
    result = []
    last_name = None
    for item in json_data:
        if item['name'] != last_name:
            result.append(item)
        last_name = item['name']
    return result

# 파일 처리 함수
def process_json_file(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    cleaned_data = remove_duplicates(data)
    
    # 변환된 데이터 저장 경로 설정
    relative_path = os.path.relpath(input_file, json_path)  # 상대 경로 계산
    output_file = os.path.join(convert_path, relative_path)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)  # 폴더 생성
    
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(cleaned_data, file, ensure_ascii=False, indent=4)

# 모든 폴더 내의 파일 처리
def process_all_json_files():
    for root, dirs, files in os.walk(json_path):
        for filename in files:
            if filename.endswith('.json'):
                input_file = os.path.join(root, filename)
                process_json_file(input_file)

# 실행
process_all_json_files()