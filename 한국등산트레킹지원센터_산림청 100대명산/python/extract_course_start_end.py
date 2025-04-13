import json
import os

# 원본 JSON 파일 경로
json_path = os.path.join(os.path.dirname(__file__), '../mnt_100_info_course.json')
# 결과 저장 경로
convert_path = os.path.join(os.path.dirname(__file__), '../convert.json')

# JSON 읽기
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 코스에서 시작과 끝만 추출
def extract_start_end(course_str):
    parts = course_str.split('→')
    parts = [p.strip() for p in parts if p.strip()]  # 공백 제거
    if len(parts) >= 2:
        return {"start": parts[0], "end": parts[-1]}
    elif len(parts) == 1:
        return {"start": parts[0], "end": parts[0]}
    else:
        return {"start": "", "end": ""}

# 각 코스 필드 처리
for item in data:
    for i in range(1, 6):
        key = f'mnt_course_{i}'
        if key in item and isinstance(item[key], str):
            item[key] = extract_start_end(item[key])

# 결과 저장
with open(convert_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("변환 완료")