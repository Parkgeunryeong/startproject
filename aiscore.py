from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
from datetime import datetime
from skyfield.api import load
from skyfield.almanac import moon_phase
import requests


app = Flask(__name__)
CORS(app)  # 외부 접근 허용

model = joblib.load("models/astro_rf_model.pkl")
scaler = joblib.load("models/astro_scaler.pkl")

#달의 밝기를 가져오는 함수
def get_moon_brightness_score(date_obj):
    eph = load('de421.bsp')
    ts = load.timescale()
    t = ts.utc(date_obj.year, date_obj.month, date_obj.day)
    phase = moon_phase(eph, t).degrees / 360.0
    return round(1 - abs(phase - 0.5) * 2, 2)

#flask서버 부분 + ai 예측 부분
@app.route("/api/predict", methods=["GET"])
def predict():
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)

    # OpenWeatherMap API-> 습도와 구름량 등등 날씨 데이터를 가져옴...
    api_key = "7c25d717157701aff47b04889930f2e2"
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    res = requests.get(url)
    if res.status_code != 200:
        return jsonify({"error": "weather fetch failed"}), 500
    data = res.json()

    # 00:00 데이터만 추출
    forecast_list = data["list"]
    filtered = [entry for entry in forecast_list if "00:00:00" in entry["dt_txt"]]

    results = []
    for entry in filtered:
        date_str = entry["dt_txt"].split(" ")[0] #날짜 추출
        date_obj = datetime.strptime(date_str, "%Y-%m-%d") #추출한 날짜를 datetime객체로 변환
        cloud = entry["clouds"]["all"] # clouds항목의 all값 추출
        humidity = entry["main"]["humidity"] # main항목의 습도(humidity)값 추출
        pop = entry.get("pop", 0.0) #강수확률 추출, 데이터값이 없을경우 0.0으로
        moon = get_moon_brightness_score(date_obj) # 해당날짜를 넣어 달밝기 함수 호출

        x = pd.DataFrame([[cloud, humidity, pop, moon]], # 머신러닝 모델 입력값
                         columns=["cloud", "humidity", "precip_prob", "moon_brightness"])
        x_scaled = scaler.transform(x) #정규화
        score = model.predict(x_scaled)[0] # 날짜의 관측 점수 socre에 저장

        results.append({ # results리스트에 결과 저장
            "date": date_str,
            "score": round(score, 2),
            "moon": moon
        })

    return jsonify(results)


if __name__ == "__main__":
    app.run()