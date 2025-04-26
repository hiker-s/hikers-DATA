import os
import json

# 경로 설정
base_dir = os.path.dirname(__file__)
json_path = os.path.join(base_dir, '../mnt_100_convert_json_2')
convert_path = os.path.join(base_dir, '../mnt_100_result/mnt_100_convert_json_clean')
os.makedirs(convert_path, exist_ok=True)

# 정제에서 제외할 산
skip_mnt = ["강천산", "황악산", "공작산", "축령산", "덕숭산", "민주지산"]


# 제거할 요소 리스트
elements_to_remove = [
    "낙석", "의약품 함", "낙뢰 및 우천시 행동 요령", "재해위험지구", 
    "추락주의", "산불감시초소", "낙석 위험", "낙석 위험지역", "사고위험지구",
    "조망점", "주차장", "위험지역", "안내표지판", "이정표", "안내도", "ㅇ", "안내판",
    "구급함", "화장실", "구조안내", "안전센터", "낙석주의", "붕괴위험지역", "119 긴급구조 넘버01-44", "입석대입구 화장실",
    "멧돼지 출몰 주의", "흡연부스", "여성전용화장실", "포토존", "고압전기시설", "좌쉼터", "오른쪽쉼터", "미끄럼주의",
    "낙석, 추락 미끄럼 주의", "자연성릉 포토스팟", "낙석 추락미끄럼주의", "미끄럼주의(상습결빙구간)", "급경사지 위험지역",
    "벤치", "갑사 입구 포토존", "급경사지 낙석 위험지역", "자연관찰로 옆 벤치", "멧돼지흔적", "야생돼지", "멧돼지출현흔적", "입산통제소", "국가지점번호",
    "나무쓰러짐", "등산로폐쇄", "낭떠러지", "추락위험"
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
    relative_path = os.path.relpath(input_file, json_path)
    mountain_name = os.path.normpath(relative_path).split(os.sep)[0].strip()

    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    if mountain_name not in skip_mnt and "track" in data:
        data["track"] = remove_element(data["track"])

    output_file = os.path.join(convert_path, relative_path)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def process_all_json_files():
    for root, dirs, files in os.walk(json_path):
        for filename in files:
            if filename.endswith('.json'):
                input_file = os.path.join(root, filename)
                process_json_file(input_file)

# 실행
process_all_json_files()