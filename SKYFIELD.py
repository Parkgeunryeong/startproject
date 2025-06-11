from skyfield.api import load, Topos
from datetime import datetime,timedelta,UTC

# 1. 천문 데이터 불러오기
eph = load('de421.bsp')  # JPL 천체 데이터
ts = load.timescale()

# 2. 날짜 설정 (현재 시간 기준)
now_utc = datetime.now(UTC)
future_utc = now_utc


t = ts.utc(future_utc.year, future_utc.month, future_utc.day, future_utc.hour, future_utc.minute)

# 3. 관측자 위치 설정 (현재 서울 기준)
observer = Topos(latitude_degrees=37.41966, longitude_degrees=126.67382)  # 그리니치 천문대 기준

# 4. 천체 위치 계산
sun = eph['sun']  # ← 태양
earth = eph['earth']
obs = earth + observer

astrometric = obs.at(t).observe(sun)
alt, az, diz = astrometric.apparent().altaz()  # 고도, 방위각, 지구부터 목성의 거리
ra, dec, _ = astrometric.radec()

# 5. 출력
print("태양의 위치:")
print("방위각 (0~360):", round(az.degrees, 2), "도")
print("고도 (-90~90):", round(alt.degrees, 2), "도")
print("지구부터 태양까지의 거리:", diz.au, "AU")

print("지금 시간",future_utc.hour)
print("적경",ra.hours);
print("적위",dec.degrees);




