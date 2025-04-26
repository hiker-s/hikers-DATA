import json
import re
import os

# 경로 설정
base_dir = os.path.dirname(__file__)
json_path = os.path.join(base_dir, '../mnt_100_course_info/mountain_info.json')
convert_dir = os.path.join(base_dir, '../mnt_100_course_info/')
convert_file = os.path.join(convert_dir, 'mountain_info_convert.json')
os.makedirs(convert_dir, exist_ok=True)

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

def replace_dot_with_newline(mnt_info):
    # 괄호 안의 .을 임시로 다른 문자로 치환하여 처리
    mnt_info = re.sub(r'\(.*?\)', lambda x: x.group(0).replace('.', '<<DOT>>'), mnt_info)

    # 문장 중간의 .을 .\n으로 변환 (마지막 . 제외)
    mnt_info = re.sub(r'\.(?!\s*$) ', '.\n', mnt_info)

    # 임시로 바꾼 <<DOT>>을 다시 .으로 복원
    mnt_info = mnt_info.replace('<<DOT>>', '.')

    return mnt_info

# JSON 데이터에서 각 "mnt_info" 필드에 대해 .을 .+줄바꿈으로 바꿈
for item in data:
    item['mnt_info'] = replace_dot_with_newline(item['mnt_info'])

# 저장
with open(convert_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)