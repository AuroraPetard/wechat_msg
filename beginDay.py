import math
import requests
import os
import random
from zhdate import ZhDate
from datetime import datetime
from wechatpy import WeChatClient, WeChatClientException
from wechatpy.client.api import WeChatMessage, WeChatTemplate

citys = os.getenv('CITY_G1').split(' ')
user_ids = os.getenv('USER_ID_G1').split(' ')
template_id = os.getenv('TEMPLATE_ID_G1')

app_id = os.getenv('APP_ID')
app_secret = os.getenv('APP_SECRET')

if app_id is None or app_secret is None:
    print('请设置 APP_ID 和 APP_SECRET')
    exit(422)

if not user_ids:
    print('请设置 USER_ID，若存在多个 ID 每行一个ID')
    exit(422)

if template_id is None:
    print('请设置 TEMPLATE_ID')
    exit(422)


def get_weather(city):
    if city is None:
        print('请设置城市')
        return None
    url = "http://t.weather.sojson.com/api/weather/city/" + city
    res = requests.get(url).json()
    if res is None:
        return get_weather(city);
    return res


week_list = [" 星期一", " 星期二", " 星期三", " 星期四", " 星期五", " 星期六", " 星期日"]


def get_week(dateTime):
    import datetime
    week = datetime.datetime.strptime(dateTime, "%Y-%m-%d").weekday()
    return week_list[week]


def get_lunar(dateTime):
    dataArr = dateTime.split("-")
    year, month, day = int(dataArr[0]), int(dataArr[1]), int(dataArr[2])
    lunar = ZhDate.from_datetime(datetime(year, month, day))
    return str(lunar)




def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)



try:
    client = WeChatClient(app_id, app_secret)
except WeChatClientException as e:
    print('微信获取 token 失败，请检查 APP_ID 和 APP_SECRET，或当日调用量是否已达到微信限制。')
    exit(502)

wm = WeChatMessage(client)

if __name__ == '__main__':
     data = {
         "day1wo":{"value":get_words(),"color":get_random_color()}
     }

     try:
         for user_id in user_ids:
             res = wm.send_template(user_id, template_id, data)
     except WeChatClientException as e:
         print('微信端返回错误：%s。错误代码：%d' % (e.errmsg, e.errcode))
         exit(502)
