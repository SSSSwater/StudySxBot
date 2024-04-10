import requests
import json

# url_root = "https://mock.apifox.com/m1/4156288-0-default/"
url_root = "http://121.196.197.146:8211/api/"
headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15"
}


def post_register(qq, name):
    param = {
        "qq": qq,
        "name": name
    }
    url = url_root + "Register"
    response = requests.post(url, data=json.dumps(param), headers=headers)
    return response


def get_register():
    url = url_root + "Register"
    response = requests.get(url, headers=headers)
    return response


def put_register(qq, name):
    param = {
        "qq": qq,
        "name": name
    }
    url = url_root + "Register/" + qq
    response = requests.put(url, params=param, headers=headers)
    return response


def delete_register(qq):
    url = url_root + "Register/" + qq
    response = requests.delete(url, headers=headers)
    return response


def post_daka(qq, pic_url, word_num):
    param = {
        "qq": qq,
        "pic_url": pic_url,
        "word_num": word_num
    }
    url = url_root + "Mark"
    response = requests.post(url, data=json.dumps(param), headers=headers)
    return response


def get_daka():
    url = url_root + "Mark"
    response = requests.get(url, headers=headers)
    return response


def post_remind_list(qq, time):
    param = {
        "qq": qq,
        "time": time
    }
    url = url_root + "Remind"
    response = requests.post(url, data=json.dumps(param), headers=headers)
    return response


def get_remind_list(qq=None):
    url = url_root + "Remind/"
    if qq:
        url += qq
    response = requests.get(url, headers=headers)
    return response


def put_remind_list(qq, time):
    param = {
        "time": time
    }
    url = url_root + "Remind/" + qq
    response = requests.put(url, params=param, headers=headers)
    return response


def delete_remind_list(qq):
    url = url_root + "Remind/" + qq
    response = requests.delete(url, headers=headers)
    return response


def get_death_list(offset=0):
    url = url_root + "Deathlist/" + str(offset)
    response = requests.get(url, headers=headers)
    return response


def get_today_list(offset=0):
    url = url_root + "Todaylist/" + str(offset)
    response = requests.get(url, headers=headers)
    return response


def get_personal_history_list(qq=None):
    url = url_root + "Marklog/"
    if qq:
        url += qq
    response = requests.get(url, headers=headers)
    return response


def test_connect():
    try:
        response = get_register()
        return json.dumps({"status": 200})
    except requests.exceptions.ConnectionError:
        return json.dumps({"status": 405})

