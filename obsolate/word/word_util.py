import json
import os
import random


def random_word():
    # with open("../../../dict/KaoYan_2.json", encoding='utf-8') as f:
    with open("dict/KaoYan_2.json", encoding='utf-8') as f:
        word_dicts = []
        for line in f.readlines():
            dic = json.loads(line)
            word_dicts.append(dic)
        num = random.randint(0, len(word_dicts) - 1)
        return {
            'word': word_dicts[num]['headWord'],
            'usphone' :'[' + word_dicts[num]['content']['word']["content"]['usphone'] + ']',
            'translates': [{
                'tranCn': tr['tranCn'],
                'position': tr['pos']} for tr in word_dicts[num]['content']['word']["content"]["trans"]],
            'sentences' : [{
                'sContent' : se['sContent'],
                'sCn': se['sCn'],
            } for se in word_dicts[num]['content']['word']["content"]["sentence"]["sentences"]]
        }