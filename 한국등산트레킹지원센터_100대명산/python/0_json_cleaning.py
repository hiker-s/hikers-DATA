import os
import json

# 경로 설정
base_dir = os.path.dirname(__file__)
json_path = os.path.join(base_dir, '../mnt_100_convert_json')
convert_path = os.path.join(base_dir, '../mnt_100_convert_json_clean')
os.makedirs(convert_path, exist_ok=True)

# 제거할 요소 리스트
elements_to_remove = [
    "낙석", "의약품 함", "낙뢰 및 우천시 행동 요령", "재해위험지구", 
    "추락주의", "산불감시초소", "낙석 위험", "낙석 위험지역", "쉼터", "사고위험지구",
    "조망점", "주차장", "위험지역", "안내표지판", "이정표", "안내도", "ㅇ", "안내판",
    "구급함", "화장실", "구조안내", "안전센터", "낙석주의", "붕괴위험지역", "119 긴급구조 넘버01-44"
]

# 불필요한 요소를 제거하는 함수
# 이름에 "갈림길"을 표현하고 있으면 뒤에 숫자를 제거하고 "갈림길"만으로 수정
    # ex) "갈림길 11", "갈림길 13", -> "갈림길"
def remove_element(json_data):
    if isinstance(json_data, list):
        cleaned = []
        for item in json_data:
            name = item.get("name", "")
            
            # 제거 조건: elements_to_remove에 포함되면 제외
            if name in elements_to_remove:
                continue
            
            # 이름 수정 조건: "갈림길"이 이름에 포함되어 있다면 이름을 "갈림길"로 변경
            if "갈림길" in name:
                item["name"] = "갈림길"
            
            cleaned.append(item)
        return cleaned
    return json_data

def process_json_file(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    # 불필요한 요소 제거
    cleaned_data = remove_element(data)
    
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