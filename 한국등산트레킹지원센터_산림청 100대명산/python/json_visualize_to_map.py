import folium
import json

# JSON 데이터 (예시로 삽입한 데이터를 변수로 사용)
data = [
    {"name": "산림문화휴양관 주차장", "lat": 37.865097, "lon": 127.981506},
    {"name": "가리산강우레이더관측소 주차장", "lat": 37.866718, "lon": 127.977547},
    {"name": "모노레일 출발/도착 정거장", "lat": 37.866898, "lon": 127.976837},
    {"name": "갈림길", "lat": 37.867962, "lon": 127.972809},
    {"name": "중간 자연쉼터", "lat": 37.87299, "lon": 127.972061},
    {"name": "갈림길", "lat": 37.873352, "lon": 127.972115},
    {"name": "중간 평지", "lat": 37.873791, "lon": 127.972488},
    {"name": "갈림길", "lat": 37.878952, "lon": 127.967575},
    {"name": "한 천자 이야기", "lat": 37.874443, "lon": 127.959641},
    {"name": "갈림길", "lat": 37.87442, "lon": 127.959267},
    {"name": "갈림길", "lat": 37.872555, "lon": 127.957832},
    {"name": "갈림길", "lat": 37.872063, "lon": 127.956665},
    {"name": "큰바위얼굴", "lat": 37.871983, "lon": 127.956566},
    {"name": "2봉", "lat": 37.872055, "lon": 127.956329},
    {"name": "3봉", "lat": 37.872437, "lon": 127.956154},
    {"name": "가리산 정상", "lat": 37.871387, "lon": 127.956276},
    {"name": "갈림길", "lat": 37.870937, "lon": 127.956886},
    {"name": "가리산 제1봉 석간수", "lat": 37.870586, "lon": 127.957031},
    {"name": "갈림길", "lat": 37.865997, "lon": 127.960678},
    {"name": "무쇠말재", "lat": 37.865925, "lon": 127.960648},
    {"name": "괴목", "lat": 37.866467, "lon": 127.963112},
    {"name": "연리목", "lat": 37.86681, "lon": 127.964844},
    {"name": "합수곡", "lat": 37.868435, "lon": 127.971527},
    {"name": "멧돼지 출몰 주의", "lat": 37.865211, "lon": 127.981049},
    {"name": "식당옆 휴양림 데크", "lat": 37.865086, "lon": 127.982491}
]

# 지도 초기화 (중앙 위치 설정)
map_center = [37.866718, 127.977547]  # 대체로 중심이 될 위도, 경도
mymap = folium.Map(location=map_center, zoom_start=15)

# 각 포인트에 마커 추가
coordinates = []
for point in data:
    # 마커 추가
    folium.Marker(
        location=[point['lat'], point['lon']],
        popup=point['name'],
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(mymap)
    
    # 좌표 리스트에 추가
    coordinates.append([point['lat'], point['lon']])

# 선으로 노드들 연결 (PolyLine)
folium.PolyLine(coordinates, color='blue', weight=2.5, opacity=1).add_to(mymap)

# 지도 HTML 파일로 저장
mymap.save("map_with_lines.html")

print("지도가 map_with_lines.html 파일로 저장되었습니다.")