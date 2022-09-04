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

user_id1 = os.environ["USER_ID1"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_wind():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  wind = res['data']['list'][0]
  return wind['wind']

def get_zhiliang():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  wind = res['data']['list'][0]
  return wind['airQuality']


def get_humidity():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  wind = res['data']['list'][0]
  return wind['humidity']

def get_weather_high():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  max_temperature = res['data']['list'][0]
  return math.floor(max_temperature['high'])

def get_weather_low():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  min_temperature = res['data']['list'][0]
  return math.floor(min_temperature['low'])



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

def get_one_words():
  onewords = requests.get("https://v1.hitokoto.cn/?c=j&c=i&c=d&c=k&c=c")
  if onewords.status_code != 200:
    return get_words()
  onestr = onewords.json()['hitokoto']
  if onewords.json()['from'] != '':
    onestr = onewords.json()['hitokoto'] + "   《" + onewords.json()['from'] +"》"
  if str(onewords.json()['from_who'])!= '':
    onestr = onewords.json()['hitokoto'] + "   --" + str(onewords.json()['from_who'])
  if onewords.json()['from'] != '' and onewords.json()['from_who'] != '':
    onestr = onewords.json()['hitokoto'] + "   《" + onewords.json()['from']+"》--" + str(onewords.json()['from_who'])
  return onestr

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"city":{"value":city,"color":"#20B2AA"},"weather":{"value":wea,"color":"#87CEFA"},"temperature":{"value":temperature,"color":"#FFB6C1"},"min_temperature":{"value":get_weather_low(),"color":"#008000"},"humidity":{"value":get_humidity()},"kongqizhiliang":{"value":get_zhiliang()},"max_temperature":{"value":get_weather_high(),"color":"#CD5C5C"},"love_days":{"value":get_count(),"color":"#9ACD32"},"birthday_left":{"value":get_birthday(),"color":"#FF0000"},"words":{"value":get_words(), "color":get_random_color()},"onewords":{"value":get_one_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
res1 = wm.send_template(user_id1, template_id, data)
print(res)
print(res1)
