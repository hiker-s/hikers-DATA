# gpx를 json으로 변환
# 최고고도와 경로정보를 json으로 반환

import os
import xml.etree.ElementTree as ET
import json

# 경로 설정
base_dir = os.path.dirname(__file__)
mnt_100_path = os.path.join(base_dir, '../mnt_100')
convert_path = os.path.join(base_dir, '../mnt_100_convert_json')
os.makedirs(convert_path, exist_ok=True)

# 네임스페이스 설정
ns = {'default': 'http://www.topografix.com/GPX/1/1'}

# 각 산 폴더 순회
for root_dir, _, files in os.walk(mnt_100_path):
    for filename in files:
        if filename.endswith('.gpx'):
            gpx_file_path = os.path.join(root_dir, filename)

            try:
                tree = ET.parse(gpx_file_path)
                root = tree.getroot()

                waypoints = []
                path_id_counter = 1
                max_ele = None

                for wpt in root.findall('default:wpt', ns):
                    lat = wpt.get('lat')
                    lon = wpt.get('lon')
                    name_elem = wpt.find('default:name', ns)
                    ele_elem = wpt.find('default:ele', ns)

                    name = name_elem.text if name_elem is not None else None
                    ele = float(ele_elem.text) if ele_elem is not None else None

                    if ele is not None:
                        if max_ele is None or ele > max_ele:
                            max_ele = ele

                    waypoints.append({
                        'path_id': path_id_counter,
                        'name': name,
                        'lat': float(lat),
                        'lon': float(lon),
                        'ele': ele
                    })
                    path_id_counter += 1

                # 최종 JSON 데이터 구성
                result = {
                    'max_ele': max_ele,
                    'track': waypoints
                }

                # 상대 경로 계산
                relative_path = os.path.relpath(gpx_file_path, mnt_100_path)
                relative_path_no_ext = os.path.splitext(relative_path)[0]

                # 파일명 가공: _ 뒤의 숫자에서 앞의 0 제거
                dirname = os.path.dirname(relative_path_no_ext)
                basename = os.path.basename(relative_path_no_ext)

                if '_' in basename:
                    name_part, num_part = basename.rsplit('_', 1)
                    try:
                        num_part_int = int(num_part)
                        new_basename = f"{name_part}_{num_part_int}"
                    except ValueError:
                        new_basename = basename
                else:
                    new_basename = basename

                # json 저장 경로 생성
                json_relative_path = os.path.join(dirname, new_basename + '.json')
                json_output_path = os.path.join(convert_path, json_relative_path)

                # 하위 디렉토리 생성
                os.makedirs(os.path.dirname(json_output_path), exist_ok=True)

                # JSON 저장
                with open(json_output_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=4)

                print(f"✅ {relative_path} 변환 완료")

            except Exception as e:
                print(f"❌ {filename} 오류 발생: {e}")