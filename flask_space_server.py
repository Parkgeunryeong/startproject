from flask import Flask, request, jsonify
from flask_cors import CORS
from skyfield.api import load, Topos
from datetime import datetime,timedelta, UTC

from SKYFIELD import astrometric

app = Flask(__name__)
CORS(app)  # 외부 접근 허용

@app.route("/api/planets", methods=["GET"])
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


    targets = [
        {"name": "Sun", "key": "sun"},
        {"name": "Jupiter", "key": "jupiter barycenter"},
        {"name": "Saturn", "key": "saturn barycenter"},
        {"name": "Mars", "key": "mars"},

    ]
    results = []
    for target in targets:
        body = eph[target["key"]]
        astrometric = obs.at(t).observe(body).apparent()
        ra, dec, _ = astrometric.radec()
        results.append({
            "label": target["name"],
            "ra": ra.hours * 15,  # degree 단위로 변환
            "dec": dec.degrees  # 그대로 degree
        })

    return jsonify(results)





if __name__ == "__main__":
    app.run(port=5000)