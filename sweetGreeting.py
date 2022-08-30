from datetime import date, datetime, timedelta
from wechatpy import WeChatClient, WeChatClientException
from wechatpy.client.api import WeChatMessage
import requests
import os
import random
import time

user_ids = os.getenv('USER_ID_GF').split(' ')
templateArr = os.getenv('TEMPLATE_ID_SG').split(' ')


t=time.localtime()

hour=t.tm_hour

if hour <= 10 :
	template_id=templateArr[0]
else:
	template_id=templateArr[1]



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



# 彩虹屁 接口不稳定，所以失败的话会重新调用，直到成功
def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']



# 随机颜色
def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


try:
    client = WeChatClient(app_id, app_secret)
except WeChatClientException as e:
    print('微信获取 token 失败，请检查 APP_ID 和 APP_SECRET，或当日调用量是否已达到微信限制。')
    exit(502)

wm = WeChatMessage(client)


data = {
    "words": {
        "value": get_words(),
        "color": get_random_color()
    },
}

if __name__ == '__main__':
    try:
        for user_id in user_ids:
            res = wm.send_template(user_id, template_id, data)
    except WeChatClientException as e:
        print('微信端返回错误：%s。错误代码：%d' % (e.errmsg, e.errcode))
        exit(502)
