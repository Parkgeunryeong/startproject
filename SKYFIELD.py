from skyfield.api import load, Topos
from datetime import datetime,UTC

# 1. 천문 데이터 불러오기
eph = load('de421.bsp')  # JPL 천체 데이터
ts = load.timescale()

# 2. 날짜 설정 (현재 시간 기준)
now = datetime.now(UTC)
t = ts.utc(now.year, now.month, now.day, now.hour, now.minute)

# 3. 관측자 위치 설정 (현재 서울 기준)
observer = Topos(latitude_degrees=37.5665, longitude_degrees=126.9780)  # 서울

# 4. 천체 위치 계산
jupiter = eph['jupiter barycenter']  # ← 목성 중심
earth = eph['earth']
obs = earth + observer

astrometric = obs.at(t).observe(jupiter)
alt, az, diz = astrometric.apparent().altaz()  # 고도, 방위각, 지구부터 목성의 거리

# 5. 출력
print("목성의 위치:")
print("방위각 (0~360):", round(az.degrees, 2), "도")
print("고도 (-90~90):", round(alt.degrees, 2), "도")
print("지구부터 목성까지의 거리:", diz.au, "AU")

print("1",observer)
print("2",earth)
print("3",obs)
print("4",astrometric)
print("5",astrometric.apparent)


