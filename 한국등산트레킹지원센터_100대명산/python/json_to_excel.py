import os
import json
import pandas as pd

# 경로 설정
base_dir = os.path.dirname(__file__)
convert_path = os.path.join(base_dir, '../mnt_100_convert_json_format')

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
                    # JSON에서 필요한 정보 추출
                    if "track" in data:
                        total_length_meter = f"{round(sum([section['length_meter'] for section in data['track']]) / 1000, 1)}km"
                        total_time = f"{sum([section['time_minute'] for section in data['track']]) // 60}시간 {sum([section['time_minute'] for section in data['track']]) % 60}분"
                        start_name = data["track"][0].get('start_name', "Unknown Start")  # 시작 지점 이름
                        end_name = data["track"][-1].get('start_name', "Unknown Start")
                        max_ele = data.get("max_ele", "Unknown")

                        # 데이터 리스트에 추가
                        data_list.append({
                            "Filename": filename,
                            "Start Name": start_name,
                            "End Name": end_name,
                            "Total Length (km)": total_length_meter,
                            "Total Time": total_time,
                            "Max Elevation": max_ele
                        })
                except Exception as e:
                    print(f"❌ {mountain_folder}/{filename} 오류 발생: {e}")

# pandas DataFrame으로 변환
df = pd.DataFrame(data_list)

# 엑셀로 저장
output_excel_path = os.path.join(base_dir, 'mountain_info.xlsx')
df.to_excel(output_excel_path, index=False, engine='openpyxl')

print(f"엑셀 파일이 생성되었습니다: {output_excel_path}")