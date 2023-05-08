import math
import requests
import os
import random
from zhdate import ZhDate
from datetime import datetime
from wechatpy import WeChatClient, WeChatClientException
from wechatpy.client.api import WeChatMessage, WeChatTemplate

citys = os.getenv('CITY_WF').split(' ')
user_ids = os.getenv('USER_ID_WF').split(' ')
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
    # url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    url = "http://t.weather.sojson.com/api/weather/city/" + city
    res = requests.get(url).json()
    if res is None:
        return None
    # weather = res['data']['list']
    return res


week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]


def get_week(dateTime):
    import datetime
    week = datetime.datetime.strptime(dateTime, "%Y-%m-%d").weekday()
    return week_list[week]


def get_lunar(dateTime):
    dataArr = dateTime.split("-")
    year, month, day = int(dataArr[0]), int(dataArr[1]), int(dataArr[2])
    lunar = ZhDate.from_datetime(datetime(year, month, day))
    return str(lunar)


# 随机颜色
def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


dontSmoke = ["吸烟易生肝肺癌 ! ! !", "吸烟==劳命伤财 ! ! !", "离香烟越近，离健康越远 ! ! !", "吸的是烟还是命 ! ! !", "祝君舍瘾把烟戒，利众益己莫迟延 ! ! !",
             "为了爱你和你爱的人，请不要吸烟 ! ! !", "现在吞云吐雾，以后病痛缠身 ! ! !", "小小一支烟，危害万万千 ! ! !", "无烟世界，清新一片 ! ! !",
             "点燃香烟的一刹那，也点燃了死亡的导火索 ! ! !", "还吸烟呢？？？ 你的肺还好吗 ! ! !", "生命只有一次，怎能断送在香烟上 ! ! !", "燃烧的是香烟，消耗的是生命 ! ! !",
             "拒绝烟草，珍爱生命 ! ! !", "吸烟是拿着你的寿命在做并不多享受的事情 ! ! !"]


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

        day1 = weatherAll['data']['forecast'][1]
        day2 = weatherAll['data']['forecast'][2]
        day3 = weatherAll['data']['forecast'][3]
        city = weatherAll['cityInfo']['city']

        data = {
            "day1c": {"value": city},

            "day1d": {"value": day1['ymd']},
            "day1w": {"value": day1['week']},
            "day1l": {"value": get_lunar(day1['ymd'])},
            "day1wa": {"value": day1['type']},
            "day1lo": {"value": day1['low']},
            "day1h": {"value": day1['high']},
            "day1wi": {"value": day1['fx']},
            "day1wl": {"value": day1['fl']},
            "day1wo": {"value": get_words(), "color": get_random_color()},

            "day2d": {"value": day2['ymd']},
            "day2w": {"value": day2['week']},
            "day2l": {"value": get_lunar(day2['ymd'])},
            "day2wa": {"value": day2['type']},
            "day2lo": {"value": day2['low'], },
            "day2h": {"value": day2['high'], },
            "day2wi": {"value": day2['fx'], },
            "day2wl": {"value": day2['fl'], },
            "day2wo": {"value": get_words(), "color": get_random_color()},

            "day3d": {"value": day3['ymd']},
            "day3w": {"value": day3['week']},
            "day3l": {"value": get_lunar(day3['ymd'])},
            "day3wa": {"value": day3['type']},
            "day3lo": {"value": day3['low']},
            "day3h": {"value": day3['high']},
            "day3wi": {"value": day3['fx']},
            "day3wl": {"value": day3['fl']},
            "day3wo": {"value": get_words(), "color": get_random_color()}
        }

        try:
            for user_id in user_ids:
                res = wm.send_template(user_id, template_id, data)
        except WeChatClientException as e:
            print('微信端返回错误：%s。错误代码：%d' % (e.errmsg, e.errcode))
            exit(502)
