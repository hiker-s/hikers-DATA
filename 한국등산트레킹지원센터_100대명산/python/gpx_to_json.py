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

                for wpt in root.findall('default:wpt', ns):
                    lat = wpt.get('lat')
                    lon = wpt.get('lon')
                    name_elem = wpt.find('default:name', ns)
                    name = name_elem.text if name_elem is not None else None

                    waypoints.append({
                        'path_id': path_id_counter,
                        'name': name,
                        'lat': float(lat),
                        'lon': float(lon)
                    })
                    path_id_counter += 1

                # 상대 경로 계산
                relative_path = os.path.relpath(gpx_file_path, mnt_100_path)
                json_relative_path = os.path.splitext(relative_path)[0] + '.json'
                json_output_path = os.path.join(convert_path, json_relative_path)

                # 하위 디렉토리 생성
                os.makedirs(os.path.dirname(json_output_path), exist_ok=True)

                # JSON 파일 저장
                with open(json_output_path, 'w', encoding='utf-8') as f:
                    json.dump(waypoints, f, ensure_ascii=False, indent=4)

                print(f"✅ {relative_path} 변환 완료")
            except Exception as e:
                print(f"❌ {filename} 오류 발생: {e}")