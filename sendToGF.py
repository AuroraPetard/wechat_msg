from datetime import date, datetime, timedelta
import math
from wechatpy import WeChatClient, WeChatClientException
from wechatpy.client.api import WeChatMessage
import requests
import os
import random
from xml.dom.minidom import parseString
from zhdate import ZhDate

city = os.getenv('CITY_GF')
user_ids = os.getenv('USER_ID_GF').split(' ')
template_id = os.getenv('TEMPLATE_ID_GF')

start_date = os.getenv('START_DATE')
birthday = os.getenv('BIRTHDAY')

app_id = os.getenv('APP_ID')
app_secret = os.getenv('APP_SECRET')

today = datetime.now() + timedelta(hours=8)

if app_id is None or app_secret is None:
    print('请设置 APP_ID 和 APP_SECRET')
    exit(422)

if not user_ids:
    print('请设置 USER_ID，若存在多个 ID 每行一个ID')
    exit(422)

if template_id is None:
    print('请设置 TEMPLATE_ID')
    exit(422)


# weather 直接返回对象，在使用的地方用字段进行调用。
def get_weather():
    if city is None:
        print('请设置城市')
        return None
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get(url).json()
    if res is None:
        return None
    weather = res['data']['list'][0]
    return weather


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


def get_more_weatherInfo():
    weather_uri = "http://wthrcdn.etouch.cn/WeatherApi?city=" + city
    resp = requests.get(weather_uri)
    if (resp.status_code == 200):
        a = resp.content
        b = a.decode("utf-8")
        dom = parseString(b)
        data = dom.documentElement
        zhishus = data.getElementsByTagName('zhishu')
        resultList = []
        for zs in zhishus:
            value = zs.getElementsByTagName('value')[0].childNodes[0].nodeValue
            detail = zs.getElementsByTagName('detail')[0].childNodes[0].nodeValue
            resultList.append([value,detail])
        return resultList


vegetables = ['拔丝土豆', '白灼菜心', '包菜炒鸡蛋粉丝', '菠菜炒鸡蛋', '炒滑蛋', '炒茄子', '炒青菜', '葱煎豆腐', '脆皮豆腐', '地三鲜', '干锅花菜', '蚝油三鲜菇', '蚝油生菜',
              '荷兰豆炒腊肠', '红烧冬瓜', '红烧茄子', '虎皮青椒', '话梅煮毛豆', '鸡蛋羹', '微波炉鸡蛋羹', '鸡蛋火腿炒黄瓜', '茄子炖土豆', '茭白炒肉', '椒盐玉米',
              '金针菇日本豆腐煲', '烤茄子', '榄菜肉末四季豆', '雷椒皮蛋', '凉拌黄瓜', '凉拌木耳', '凉拌莴笋', '凉拌油麦菜', '麻婆豆腐', '蒲烧茄子', '芹菜拌茶树菇', '陕北熬豆角',
              '上汤娃娃菜', '手撕包菜', '水油焖蔬菜', '素炒豆角', '酸辣土豆丝', '糖拌西红柿', '莴笋叶煎饼', '西红柿炒鸡蛋', '西红柿豆腐汤羹', '西葫芦炒鸡蛋', '洋葱炒鸡蛋']

meats = ['白菜猪肉炖粉条', '番茄红酱', '干煸仔鸡', '宫保鸡丁', '咕噜肉', '黑椒牛柳', '简易红烧肉', '南派红烧肉', '红烧猪蹄', '湖南家常红烧肉', '黄瓜炒肉', '黄焖鸡', '徽派红烧肉',
         '回锅肉', '尖椒炒牛肉', '姜炒鸡', '姜葱捞鸡', '酱牛肉', '酱排骨', '咖喱肥牛', '可乐鸡翅', '口水鸡', '辣椒炒肉', '老式锅包肉', '冷吃兔', '荔枝肉', '凉拌鸡丝',
         '萝卜炖羊排', '麻辣香锅', '麻婆豆腐', '梅菜扣肉', '啤酒鸭', '瘦肉土豆片', '水煮牛肉', '水煮肉片', '蒜苔炒肉末', '台式卤肉饭', '糖醋里脊', '糖醋排骨', '土豆炖排骨',
         '无骨鸡爪', '西红柿牛腩', '西红柿土豆炖牛肉', '乡村啤酒鸭', '香干芹菜炒肉', '香干肉丝', '香菇滑鸡', '香煎五花肉', '小炒黄牛肉', '小炒肉', '新疆大盘鸡', '血浆鸭',
         '羊排焖面', '洋葱炒猪肉', '鱼香茄子', '鱼香肉丝', '猪皮冻', '猪肉烩酸菜', '柱候牛腩', '孜然牛肉', '醉排骨', '白灼虾', '鳊鱼炖豆腐', '蛏抱蛋', '葱烧海参', '葱油桂鱼',
         '干煎阿根廷红虾', '红烧鲤鱼', '红烧鱼', '红烧鱼头', '黄油煎虾', '烤鱼', '咖喱炒蟹', '鲤鱼炖白菜', '清蒸鲈鱼', '清蒸生蚝', '水煮鱼', '蒜蓉虾', '糖醋鲤鱼',
         '微波葱姜黑鳕鱼', '香煎翘嘴鱼', '小龙虾', '油焖大虾']

mainFoods = ['鸡蛋三明治', '煎饺', '金枪鱼酱三明治', '美式炒蛋', '牛奶燕麦', '水煮玉米', '吐司果酱', '微波炉蛋糕', '燕麦鸡蛋饼', '炒方便面', '炒河粉', '炒凉粉', '炒馍',
             '炒年糕', '炒意大利面', '蛋炒饭', '豆角焖面', '韩式拌饭', '河南蒸面条', '基础牛奶面包', '茄子肉煎饼', '鲣鱼海苔玉米饭', '酱拌荞麦面', '空气炸锅照烧鸡饭', '醪糟小汤圆',
             '老干妈拌面', '老友猪肉粉', '烙饼', '凉粉', '麻辣减脂荞麦面', '麻油拌面', '电饭煲蒸米饭', '煮锅蒸米饭', '披萨饼皮', '热干面', '日式咖喱饭', '烧饼', '手工水饺',
             '酸辣蕨根粉', '汤面', '微波炉腊肠煲仔饭', '西红柿鸡蛋挂面', '扬州炒饭', '炸酱面', '蒸卤面', '中式馅饼', '速冻馄饨', '煮泡面加蛋']

soups = ['鲫鱼豆腐汤', '勾芡香菇汤', '金针菇汤', '米粥', '皮蛋瘦肉粥', '生汆丸子汤', '西红柿鸡蛋汤', '小米粥', '银耳莲子粥', '紫菜蛋花汤', '桂圆红枣粥']


def get_foods():
    return [random.choice(vegetables), random.choice(meats), random.choice(mainFoods), random.choice(soups)]


# 纪念日正数
def get_memorial_days_count():
    if start_date is None:
        print('没有设置 START_DATE')
        return 0
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


# 生日倒计时
def get_birthday_left():
    if birthday is None:
        print('没有设置 BIRTHDAY')
        return 0
    next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days


# 彩虹屁 接口不稳定，所以失败的话会重新调用，直到成功
def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


def format_temperature(temperature):
    return math.floor(temperature)


# 随机颜色
def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


try:
    client = WeChatClient(app_id, app_secret)
except WeChatClientException as e:
    print('微信获取 token 失败，请检查 APP_ID 和 APP_SECRET，或当日调用量是否已达到微信限制。')
    exit(502)

wm = WeChatMessage(client)
weather = get_weather()
if weather is None:
    print('获取天气失败')
    exit(422)

moreInfo = get_more_weatherInfo()
if moreInfo is None:
    print('获取更多信息失败')
    exit(422)

foods = get_foods()



data = {
    "city": {
        "value": city,
        "color": get_random_color()
    },
    "date": {
        "value": today.strftime('%Y年%m月%d日'),
        "color": get_random_color()
    },
    "week": {
        "value": get_week(weather['date']),
        "color": get_random_color()
    },
    "lunar": {
        "value": get_lunar(weather['date']),
        "color": get_random_color()
    },
    "weather": {
        "value": weather['weather'],
        "color": get_random_color()
    },
    "temperature": {
        "value": math.floor(weather['temp']),
        "color": get_random_color()
    },
    "highest": {
        "value": math.floor(weather['high']),
        "color": get_random_color()
    },
    "lowest": {
        "value": math.floor(weather['low']),
        "color": get_random_color()
    },
    "clothers": {
        "value": moreInfo[0][1],
        "color": get_random_color()
    },
    "UVI": {
        "value": moreInfo[1][1],
        "color": get_random_color()
    },
    "skinCare": {
        "value": moreInfo[2][1],
        "color": get_random_color()
    },
    "cold": {
        "value": moreInfo[4][1],
        "color": get_random_color()
    },
    "dry": {
        "value": moreInfo[5][0],
        "color": get_random_color()
    },
    "outdoor": {
        "value": moreInfo[6][0],
        "color": get_random_color()
    },
    "pollution": {
        "value": moreInfo[7][0],
        "color": get_random_color()
    },
    "sunstroke": {
        "value": moreInfo[9][0],
        "color": get_random_color()
    },
    "comfort": {
        "value": moreInfo[10][0],
        "color": get_random_color()
    },
    "vege": {
        "value": foods[0],
        "color": get_random_color()
    },
    "meat": {
        "value": foods[1],
        "color": get_random_color()
    },
    "mainFood": {
        "value": foods[2],
        "color": get_random_color()
    },
    "soup": {
        "value": foods[3],
        "color": get_random_color()
    },
    "love_days": {
        "value": get_memorial_days_count(),
        "color": get_random_color()
    },
    "birthday_left": {
        "value": get_birthday_left(),
        "color": get_random_color()
    },
    "words": {
        "value": get_words(),
        "color": get_random_color()
    },
}

if __name__ == '__main__':
    count = 0
    try:
        for user_id in user_ids:
            res = wm.send_template(user_id, template_id, data)
            count += 1
    except WeChatClientException as e:
        print('微信端返回错误：%s。错误代码：%d' % (e.errmsg, e.errcode))
        exit(502)

    print("发送了" + str(count) + "条消息")
