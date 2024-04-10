import json

import requests

# url_root = "https://mock.apifox.com/m1/4156288-0-default/"
url_root = "http://121.196.197.146:8211/api/"
headers = {
    "Content-Type": "image/jpeg",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15"
}


def get_H():
    url = url_root + "H"
    response = requests.get(url, headers=headers)
    return response


def post_H(pic_url):
    param = {
        "pic_url": pic_url
    }
    url = url_root + "H"
    response = requests.post(url, data=json.dumps(param), headers=headers)
    return response
