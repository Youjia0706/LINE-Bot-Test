import requests
import json
from datetime import datetime

with open("setting.json", "r", encoding="utf-8") as f:
    settings = json.load(f)

api_key = settings["CWB_API_KEY"]

def get_rain_chance(city_name, api_key):
    url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"
    params = {
        "Authorization": api_key,
        "locationName": city_name
    }
    resp = requests.get(url, params=params)
    data = resp.json()

    try:
        location_data = data["records"]["location"][0]
    except (KeyError, IndexError):
        return None  # 找不到城市
    rain_list = []
    # 找到 PoP (降雨機率) 資料
    for element in location_data["weatherElement"]:
        if element["elementName"] == "PoP":  # 降雨機率
            for time_info in element["time"]:
                start = time_info["startTime"]
                end = time_info["endTime"]
                chance = time_info["parameter"]["parameterName"]
                rain_list.append({
                    "start": start,
                    "end": end,
                    "chance": chance
                })
            break

    return rain_list if rain_list else None


def format_time(time_str):
    dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    return f"{dt.month}/{dt.day} {dt.hour:02d}:{dt.minute:02d}"

# 測試
if __name__ == "__main__":
    city = "新北市"
    rain_schedule = get_rain_chance(city, api_key)
    if rain_schedule:
        print(f"{city} 未來降雨預報：")
        for period in rain_schedule:
            print(f"{period['start']} ~ {period['end']} ： {period['chance']}%")
    else:
        print(f"{city} 明天不會下雨")
