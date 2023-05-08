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

        d1 = weatherAll['data']['forecast'][1]
        d2 = weatherAll['data']['forecast'][2]
        d3 = weatherAll['data']['forecast'][3]

        data = {
            "d1c": {"value": weatherAll['cityInfo']['city']},
            "d1d": {"value": d1['ymd']},
            "d1w": {"value": d1['week']},
            "d1l": {"value": get_lunar(d1['ymd'])},
            "d1wa": {"value": d1['type']},
            "d1lo": {"value": d1['low']},
            "d1h": {"value": d1['high']},
            "d1wi": {"value": d1['fx']},
            "d1wl": {"value": d1['fl']},
            "d1wo": {"value": get_words(), "color": get_random_color()},
            "d2c": {"value": weatherAll['cityInfo']['city'], },
            "d2d": {"value": d2['ymd']},
            "d2w": {"value": d2['week']},
            "d2l": {"value": get_lunar(d2['ymd']), },
            "d2wa": {"value": d2['type'], },
            "d2lo": {"value": d2['low'], },
            "d2h": {"value": d2['high'], },
            "d2wi": {"value": d2['fx'], },
            "d2wl": {"value": d2['fl'], },
            "d2wo": {"value": get_words(), "color": get_random_color()},
            "d3c": {"value": weatherAll['cityInfo']['city']},
            "d3d": {"value": d3['ymd']},
            "d3w": {"value": d3['week']},
            "d3l": {"value": get_lunar(d3['ymd'])},
            "d3wa": {"value": d3['type']},
            "d3lo": {"value": d3['low']},
            "d3h": {"value": d3['high']},
            "d3wi": {"value": d3['fx']},
            "d3wl": {"value": d3['fl']},
            "d3wo": {"value": get_words(), "color": get_random_color()}
        }

        try:
            for user_id in user_ids:
                res = wm.send_template(user_id, template_id, data)
        except WeChatClientException as e:
            print('微信端返回错误：%s。错误代码：%d' % (e.errmsg, e.errcode))
            exit(502)
