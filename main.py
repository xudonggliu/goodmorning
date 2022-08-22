from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "https://devapi.qweather.com/v7/weather/now?location=101180708&key=82f4bdcbb85e47e3ae1a136aace1c8e2" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_weather_text():
  url = "https://devapi.qweather.com/v7/weather/now?location=101180708&key=82f4bdcbb85e47e3ae1a136aace1c8e2" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['weather'])


def get_weather_high():
  url = "https://devapi.qweather.com/v7/weather/now?location=101180708&key=82f4bdcbb85e47e3ae1a136aace1c8e2" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['high'])

def get_weather_low():
  url = "https://devapi.qweather.com/v7/weather/now?location=101180708&key=82f4bdcbb85e47e3ae1a136aace1c8e2" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['low'])



def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"min_temperature":{"value":get_weather_low()},"max_temperature":{"value":get_weather_high()},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
