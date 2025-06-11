from skyfield.api import load, Topos
from datetime import datetime, timedelta, UTC

# 천체 데이터 로드
eph = load('de421.bsp')
ts = load.timescale()
observer = Topos(latitude_degrees=37.5665, longitude_degrees=126.9780)  # 서울

# 시간 1: 현재 시각 (UTC + 9 = KST)
now1 = datetime.now(UTC) + timedelta(hours=9)
t1 = ts.utc(now1.year, now1.month, now1.day, now1.hour, now1.minute)

# 시간 2: 2시간 전 (시차 비교용)
now2 = now1 - timedelta(hours=2)
t2 = ts.utc(now2.year, now2.month, now2.day, now2.hour, now2.minute)

# 천체 (예: 목성)
jupiter = eph['jupiter barycenter']
earth = eph['earth']
obs = earth + observer

# 관측 시점 1
astro1 = obs.at(t1).observe(jupiter).apparent()
ra1, dec1, _ = astro1.radec()
alt1, az1, _ = astro1.altaz()

# 관측 시점 2
astro2 = obs.at(t2).observe(jupiter).apparent()
ra2, dec2, _ = astro2.radec()
alt2, az2, _ = astro2.altaz()

# 결과 출력
print("=== 적경/적위 비교 ===")
print(f"RA1: {ra1.hours:.5f}h, Dec1: {dec1.degrees:.5f}°")
print(f"RA2: {ra2.hours:.5f}h, Dec2: {dec2.degrees:.5f}°")
print(f"→ 차이: RA {abs(ra1.hours - ra2.hours):.5f}h, Dec {abs(dec1.degrees - dec2.degrees):.5f}°")

print("\n=== 방위각/고도 비교 ===")
print(f"시점 1 → Az: {az1.degrees:.2f}°, Alt: {alt1.degrees:.2f}°")
print(f"시점 2 → Az: {az2.degrees:.2f}°, Alt: {alt2.degrees:.2f}°")
print(f"→ 차이: Az {abs(az1.degrees - az2.degrees):.2f}°, Alt {abs(alt1.degrees - alt2.degrees):.2f}°")