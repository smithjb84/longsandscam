import requests

def get_weather():
    
    API_KEY = ""
    r = requests.get(("http://api.openweathermap.org/data/2.5/weather?q=tynemouth&appid={}&units=metric".format(API_KEY)).json()

    emoti = {
        "Clear": "\U00002600",
        "Clouds": "\U00002601",
        "Drizzle": "\U0001F326",
        "Rain": "\U0001F327",
        "Thunderstorm": "\U0001F329",
        "Snow": "\U0001F328",
        "Mist": "\U0001F32B",
    }

    direction = {
        "S": "\U00002B06",
        "SW": "\U00002197",
        "W": "\U000027A1",
        "NW": "\U00002198",
        "N": "\U00002B07",
        "NE": "\U00002199",
        "E": "\U00002B05",
        "SE": "\U00002196",
    }

    temp = r["main"]["temp"]
    description = r["weather"][0]["main"]
    wind_dir = r["wind"]["deg"]
    wind_speed = r["wind"]["speed"]
    emoticon_weather = emoti[description]

    if 338 < wind_dir < 22:
        dir_emoj = "N"
    elif 23 < wind_dir < 67:
        dir_emoj = "NE"
    elif 68 < wind_dir < 112:
        dir_emoj = "E"
    elif 113 < wind_dir < 157:
        dir_emoj = "SE"
    elif 158 < wind_dir < 202:
        dir_emoj = "S"
    elif 203 < wind_dir < 247:
        dir_emoj = "SW"
    elif 248 < wind_dir < 292:
        dir_emoj = "W"
    else:
        dir_emoj = "NW"

    emoticon_wind = direction[dir_emoj]

    return(temp, description, wind_speed, dir_emoj, emoticon_weather, emoticon_wind)
