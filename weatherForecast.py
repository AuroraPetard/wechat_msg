import math
import requests
import os
import random
from zhdate import ZhDate
from datetime import datetime
from wechatpy import WeChatClient, WeChatClientException
from wechatpy.client.api import WeChatMessage

citys = os.getenv('CITY_WF').split("\n")
user_ids = os.getenv('USER_ID_WF').split("\n")
template_id = os.getenv('TEMPLATE_ID_WF')


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
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get(url).json()
    if res is None:
        return None
    weather = res['data']['list']
    return weather


week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]


def get_week(dateTime):
    import datetime
    week = datetime.datetime.strptime(dateTime, "%Y-%m-%d").weekday()
    return week_list[week]


def get_lunar(dateTime):
    dataArr = dateTime.split("-")
    year, month, day = int(dataArr[0]), int(dataArr[1]), int(dataArr[2])
    return ZhDate.from_datetime(datetime(year, month, day))


# 随机颜色
def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


dontSmoke=["吸烟易生肝肺癌 ! ! !","吸烟==劳命伤财 ! ! !","离香烟越近，离健康越远 ! ! !","吸的是烟还是命 ! ! !","祝君舍瘾把烟戒，利众益己莫迟延 ! ! !","为了爱你和你爱的人，请不要吸烟 ! ! !","现在吞云吐雾，以后病痛缠身 ! ! !","小小一支烟，危害万万千 ! ! !","无烟世界，清新一片 ! ! !","点燃香烟的一刹那，也点燃了死亡的导火索 ! ! !","还吸烟呢？？？ 你的肺还好吗 ! ! !","生命只有一次，怎能断送在香烟上 ! ! !","燃烧的是香烟，消耗的是生命 ! ! !","拒绝烟草，珍爱生命 ! ! !","吸烟是拿着你的寿命在做并不多享受的事情 ! ! !"]
def get_words():
	return random.choice(dontSmoke)
	

try:
    client = WeChatClient(app_id, app_secret)
except WeChatClientException as e:
    print('微信获取 token 失败，请检查 APP_ID 和 APP_SECRET，或当日调用量是否已达到微信限制。')
    exit(502)

wm = WeChatMessage(client)

if __name__ == '__main__':
    for city in citys:
        weatherAll = get_weather(city)

        d1 = weatherAll[1]
        d2 = weatherAll[2]
        d3 = weatherAll[3]

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
        try:
            for user_id in user_ids:
                res = wm.send_template(user_id, template_id, data)
        except WeChatClientException as e:
            print('微信端返回错误：%s。错误代码：%d' % (e.errmsg, e.errcode))
            exit(502)
