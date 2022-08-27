import math
import requests
import os
import random
from zhdate import ZhDate
from datetime import datetime


os.environ["CITY"] = "北京\n天津"

citys = os.getenv('CITY').split("\n")

def get_weather(city):
  if city is None:
    print('请设置城市')
    return None
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  if res is None:
    return None
  weather = res['data']['list']
  return weather



week_list = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
def get_week(dateTime):
	import datetime
	week = datetime.datetime.strptime(dateTime, "%Y-%m-%d").weekday()
	return week_list[week]



def get_lunar(dateTime):
	dataArr=dateTime.split("-")
	year,month,day=int(dataArr[0]),int(dataArr[1]),int(dataArr[2])
	return ZhDate.from_datetime(datetime(year, month,day))


# 随机颜色
def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


# 彩虹屁 接口不稳定，所以失败的话会重新调用，直到成功
def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']



if __name__ == '__main__':
	for city in citys:
		weatherAll = get_weather(city)
		
		d1=weatherAll[1]
		d2=weatherAll[2]
		d3=weatherAll[3]
		
		data = {
		  "d1_city": {
		    "value": d1['city'],
		    "color": get_random_color()
		  },
		  "d1_date": {
		    "value": d1['date'],
		    "color": get_random_color()
		  },
		  "week_d1_date": {
		    "value": get_week(d1['date']),
		    "color": get_random_color()
		  },
		  "lunar_d1_date": {
		    "value": get_lunar(d1['date']),
		    "color": get_random_color()
		  },
		  "d1_weather": {
		    "value": d1['weather'],
		    "color": get_random_color()
		  },
		  "d1_low": {
		    "value": math.floor(d1['low']),
		    "color": get_random_color()
		  },
		  "d1_high": {
		    "value": math.floor(d1['high']),
		    "color": get_random_color()
		  },
		  "d1_wind": {
		    "value": d1['wind'],
		    "color": get_random_color()
		  },
		  "d1_windLevel": {
		    "value": d1['windLevel'],
		    "color": get_random_color()
		  },
		  "d1_airQuality": {
		    "value": d1['airQuality'],
		    "color": get_random_color()
		  },
		  "d1_words": {
		    "value": get_words(),
		    "color": get_random_color()
		  },
		  "d2_city": {
		    "value": d2['city'],
		    "color": get_random_color()
		  },
		  "d2_date": {
		    "value": d2['date'],
		    "color": get_random_color()
		  },
		  "week_d2_date": {
		    "value": get_week(d2['date']),
		    "color": get_random_color()
		  },
		  "lunar_d2_date": {
		    "value": get_lunar(d2['date']),
		    "color": get_random_color()
		  },
		  "d2_weather": {
		    "value": d2['weather'],
		    "color": get_random_color()
		  },
		  "d2_low": {
		    "value": math.floor(d2['low']),
		    "color": get_random_color()
		  },
		  "d2_high": {
		    "value": math.floor(d2['high']),
		    "color": get_random_color()
		  },
		  "d2_wind": {
		    "value": d2['wind'],
		    "color": get_random_color()
		  },
		  "d2_windLevel": {
		    "value": d2['windLevel'],
		    "color": get_random_color()
		  },
		  "d2_airQuality": {
		    "value": d2['airQuality'],
		    "color": get_random_color()
		  },
		  "d2_words": {
		    "value": get_words(),
		    "color": get_random_color()
		  },
		  "d3_city": {
		    "value": d3['city'],
		    "color": get_random_color()
		  },
		  "d3_date": {
		    "value": d3['date'],
		    "color": get_random_color()
		  },
		  "week_d3_date": {
		    "value": get_week(d3['date']),
		    "color": get_random_color()
		  },
		  "lunar_d3_date": {
		    "value": get_lunar(d3['date']),
		    "color": get_random_color()
		  },
		  "d3_weather": {
		    "value": d3['weather'],
		    "color": get_random_color()
		  },
		  "d3_low": {
		    "value": math.floor(d3['low']),
		    "color": get_random_color()
		  },
		  "d3_high": {
		    "value": math.floor(d3['high']),
		    "color": get_random_color()
		  },
		  "d3_wind": {
		    "value": d3['wind'],
		    "color": get_random_color()
		  },
		  "d3_windLevel": {
		    "value": d3['windLevel'],
		    "color": get_random_color()
		  },
		  "d3_airQuality": {
		    "value": d3['airQuality'],
		    "color": get_random_color()
		  },
		  "d3_words": {
		    "value": get_words(),
		    "color": get_random_color()
		  },
		}
		print(data)
		print("\n")
