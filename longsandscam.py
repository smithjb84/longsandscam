import requests
from bs4 import BeautifulSoup
import json
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os
from time import sleep
from instagrapi import Client, types
import datetime
from weather import get_weather

BASE_URL = "https://magicseaweed.com/Tynemouth-Longsands-Surf-Report/26/"
CAMERA = 2
VIDEO_CLIP_LENGTH = 30  # Seconds
POST_FREQUENCY = 120  # Minutes
START_TIME = 8
END_TIME = 16
PAST_URL = ""

USERNAME = ''
PASSWORD = ''

cl = Client()
cl.login(USERNAME, PASSWORD)

while True:
    try:
        try:
            os.remove("surf.mp4")
        except:
            print("no file")
        try:
            os.remove("surf.mp4.jpg")
        except:
            print("no file")
        now = datetime.datetime.now().time()
        if datetime.time(START_TIME) < now < datetime.time(END_TIME):
            r = requests.get(BASE_URL)
            soup = BeautifulSoup(r.text, 'html.parser')

            div = soup.findAll("div", {"class": "msw-fc"})
            block = div[0]["data-cam"]
            json_block = json.loads(block)
            video_url = json_block["image"]["panoramic"]["positions"][CAMERA-1]["video"]["url"]

            if video_url != PAST_URL:
                PAST_URL = video_url
                filename = video_url.split('/')[-1]

                with requests.get(video_url, stream=True) as r:
                    r.raise_for_status()
                    with open(filename, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                ffmpeg_extract_subclip(filename, 0, VIDEO_CLIP_LENGTH, targetname="surf.mp4")

                os.remove(filename)
                path = os.path.abspath("surf.mp4")

                nowstring = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")

                temp, description, wind_speed, dir, emoticon_weather, emoticon_wind = get_weather()

                cl.video_upload(path, "{} currently {} degC {} {} Wind Speed {} {} {} #tynemouth #tynemouthlongsands #surfing #forecast #longsands"
                                      "#longsandsbeach #longsandssurf".format(nowstring, temp, description,
                                                                                              emoticon_weather, wind_speed,
                                                                                              dir, emoticon_wind))
    except:
        print("something went wrong")

    print("sleeping for {} minutes".format(POST_FREQUENCY))
    sleep(POST_FREQUENCY*60)
