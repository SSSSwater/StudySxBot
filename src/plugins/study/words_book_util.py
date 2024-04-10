import json

import requests
import ECDICT.dictutils as du
url_root = "https://api.frdic.com/api/open/v1/studylist/"
headers = {
    "Content-Type": "application/json",
    "Authorization": "NIS dNNfC6diMFY2HgQpQnMv9pHXFLsJMQSuyEZl5PaWZHDjk2z9dVhVNQ==",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15"
}

appid = "HNyz7OL6khHgn5zxsC7L6irCVbmWoOPI"
appSecurity = "AKUpXM8kuUAvlyoKyNoNZOfXdOkwU5EW"


def get_book():
    url = url_root + "category"

    param = {
        "language": "en"
    }
    response = requests.get(url, params=param, headers=headers)
    return response


def get_words():
    url = url_root + "words/0"
    dg = du.Generator()
    print(dg.word_tag(data="ky"))
    param = {
        "id": "0",
        "language": "en",
        "page": "0"
    }
    response = requests.get(url, params=param, headers=headers)
    return response

def post_words(words):
    url = url_root + "words"

    param = {
        "id": "0",
        "language": "en",
        "words": words
    }
    response = requests.post(url, data=json.dumps(param), headers=headers)
    return response


get_words()
