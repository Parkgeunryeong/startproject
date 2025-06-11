from skyfield.api import load, Topos
from datetime import datetime, timedelta, UTC

# 1. 천체 데이터 로드
eph = load('de421.bsp')
ts = load.timescale()
observer = Topos(latitude_degrees=37.5665, longitude_degrees=126.9780)  # 서울

# 2. 시각 설정 (KST → UTC로 변환)
# 오전 6시 (KST → UTC = 전날 21시)
time1 = datetime.now(UTC).replace(hour=21, minute=0, second=0, microsecond=0)
# 오전 10시 (KST → UTC = 다음날 01시)
time2 = time1 + timedelta(hours=4)

t1 = ts.utc(time1.year, time1.month, time1.day, time1.hour, time1.minute)
t2 = ts.utc(time2.year, time2.month, time2.day, time2.hour, time2.minute)

# 3. 천체 위치 계산
sun = eph['sun']
earth = eph['earth']
obs = earth + observer

astro1 = obs.at(t1).observe(sun).apparent()
ra1, dec1, _ = astro1.radec()
alt1, az1, _ = astro1.altaz()

astro2 = obs.at(t2).observe(sun).apparent()
ra2, dec2, _ = astro2.radec()
alt2, az2, _ = astro2.altaz()

# 4. 출력
print("=== 적경/적위 비교 ===")
print(f"RA1 (06시): {ra1.hours:.5f}h, Dec1: {dec1.degrees:.5f}°")
print(f"RA2 (10시): {ra2.hours:.5f}h, Dec2: {dec2.degrees:.5f}°")
print(f"→ RA 차이: {abs(ra1.hours - ra2.hours):.5f}h")
print(f"→ Dec 차이: {abs(dec1.degrees - dec2.degrees):.5f}°")

print("\n=== 방위각/고도 비교 ===")
print(f"06시 → Az: {az1.degrees:.2f}°, Alt: {alt1.degrees:.2f}°")
print(f"10시 → Az: {az2.degrees:.2f}°, Alt: {alt2.degrees:.2f}°")
print(f"→ Az 차이: {abs(az1.degrees - az2.degrees):.2f}°, Alt 차이: {abs(alt1.degrees - alt2.degrees):.2f}°")