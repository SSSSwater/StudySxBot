import json
import os
from io import BytesIO
from PIL import Image

import requests

url_root = "http://localhost:5555/"
url_root = "http://121.43.164.15:5555/"
headers = {
    "Content-Type": "image/jpeg",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15"
}


def get_H(qq=None):
    url = url_root + "H/"
    if qq:
        url += qq
    response = requests.get(url, headers=headers)
    return response


def post_H(pic_url, qq):
    url = url_root + "H/" + qq
    resp = requests.get(pic_url, stream=True)
    if not os.path.exists('h_temp'):
        os.makedirs('h_temp')
    fp = 'h_temp/' + qq
    with open(fp, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=1024):
            f.write(chunk)
    try:
        img = Image.open(fp)
    except Exception as e:
        return {'code':405, 'msg': str(e.args)}
    path = fp + '.' + img.format.lower()
    img.close()
    os.rename(fp, path)
    res = None
    with open(path, 'rb') as f:
        res = requests.post(url, files={'file': f})
    os.remove(path)
    return {'code':res.status_code, 'msg': ""}

def get_nickname(qq):
    param = {
        'qq' : qq
    }
    response = requests.get("https://api.oioweb.cn/api/qq/info",params=param)
    return response.json()['result']['nickname']

test_url = "https://gchat.qpic.cn/gchatpic_new/0/0-0-197E65B4FAFA4AAF4280D4ED1481358C/0?term=2"
print(get_nickname("307722647"))