from flask import Flask, request, jsonify
from flask_cors import CORS
from skyfield.api import load, Topos
from datetime import datetime,timedelta, UTC

from SKYFIELD import astrometric

app = Flask(__name__)
CORS(app)  # 외부 접근 허용

@app.route("/api/jupiter", methods=["GET"])
def jupiter_position():
    # 요청 파라미터: 위도, 경도
    lat = float(request.args.get("lat"))
    lon = float(request.args.get("lon"))

    # 천체 데이터 로드
    eph = load('de421.bsp')
    ts = load.timescale()
    now = datetime.now(UTC)
    t = ts.utc(now.year, now.month, now.day, now.hour, now.minute)

    # 관측자 위치
    observer = Topos(latitude_degrees=lat, longitude_degrees=lon)
    obs = eph["earth"] + observer
    jupiter = eph["sun"]

    # 위치 계산
    #astrometric = obs.at(t).observe(jupiter)
    #alt, az, dist = astrometric.apparent().altaz()
    astrometric = obs.at(t).observe(jupiter).apparent()
    ra, dec, _ = astrometric.radec()

    ra_degrees = ra.hours * 15

    return jsonify({
        "ra": ra_degrees,  # 적경 (시간 단위 → float)
        "dec": dec.degrees,  # 적위 (도 단위 → float)
        "label": "Sun"
    })

    # 결과 응답
    #return jsonify({
    #    "azimuth": round(az.degrees, 2),      # 방위각 (0~360도)
    #    "altitude": round(alt.degrees, 2),    # 고도 (-90~90도)
    #    "distance_au": round(dist.au, 4)      # 지구-목성 거리 (천문단위)
    #})



if __name__ == "__main__":
    app.run(port=5000)