import os
import json
import random
import math

# 경로 설정
base_dir = os.path.dirname(__file__)
json_path = os.path.join(base_dir, '../mnt_100_convert_json_format')
convert_path = os.path.join(base_dir, '../mnt_100_convert_json_add_info')
os.makedirs(convert_path, exist_ok=True)

# start_point_name / end_point_name / total_length / total_time / max_ele