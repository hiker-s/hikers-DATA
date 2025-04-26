import os
import json
import pandas as pd

# 경로 설정
base_dir = os.path.dirname(__file__)
convert_path = os.path.join(base_dir, '../mnt_100_result/mnt_100_convert_json_format_add_level')

# 엑셀로 저장할 데이터 리스트
data_list = []

# 각 산 이름의 폴더 순회
for mountain_folder in os.listdir(convert_path):
    mountain_path = os.path.join(convert_path, mountain_folder)

    if os.path.isdir(mountain_path):
        # 각 산 이름의 폴더 안의 JSON 파일 순회
        for filename in os.listdir(mountain_path):
            if filename.endswith('.json'):
                input_file_path = os.path.join(mountain_path, filename)

                try:
                    # JSON 파일 읽기
                    with open(input_file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    # JSON에서 필요한 정보 추출
                    if "track" in data:
                        courseId = data["course_id"]
                        mntId = data["mnt_id"]
                        courseFilePath = f"{mountain_folder}/{filename}"
                        courseLastLat = data["track"][-1]["path"][-1].get("lat")
                        courseLastLng = data["track"][-1]["path"][-1].get("lng")

                        # 데이터 리스트에 추가
                        data_list.append({
                            "courseId": courseId,
                            "mntId": mntId,
                            "courseFilePath": courseFilePath,
                            "courseLastLat": courseLastLat,
                            "courseLastLng": courseLastLng
                        })

                except Exception as e:
                    print(f"❌ {mountain_folder}/{filename} 오류 발생: {e}")

# pandas DataFrame으로 변환
df = pd.DataFrame(data_list)

# 엑셀로 저장
output_excel_path = os.path.join(base_dir, '../mnt_100_result/course_info.xlsx')
df.to_excel(output_excel_path, index=False, engine='openpyxl')

print(f"엑셀 파일 생성")