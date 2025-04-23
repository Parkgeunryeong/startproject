#  필요한 모듈 불러오기
from skyfield.api import load
from skyfield.almanac import moon_phase

# 시간대 설정
ts = load.timescale()
eph = load('de421.bsp')  # NASA의 천체 위치 데이터
print(eph)


#  달 위상 계산 함수
def get_moon_phase_fraction(year, month, day):
    t = ts.utc(year, month, day)
    phase_angle = moon_phase(eph, t).degrees  # 0~360도 사이
    return round(phase_angle / 360.0, 2)  # 0~1로 정규화

#  날짜 입력
phase = get_moon_phase_fraction(2025, 4, 14)
print("달 위상각도를 정규화한 값 (0~1):", phase)

moon_visibility_score = round(1 - abs(phase - 0.5) * 2, 2)


print("달위상 점수 1은 보름달 , 0는 신월",moon_visibility_score)
