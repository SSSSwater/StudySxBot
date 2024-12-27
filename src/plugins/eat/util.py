import json
import os
import random
import requests
from scipy.special import comb
import openai


def random_10(group_id):
    if not os.path.exists("recipe"):
        os.makedirs("recipe")
    rec_dir = "recipe/recipe_" + str(group_id) + ".txt"
    if not os.path.exists(rec_dir):
        return []
    with open(rec_dir, "r", encoding='utf-8') as f:
        food_list = f.read().split('\n')
        food_list = list(filter(lambda x:x!='',food_list))
        select_food = random.sample(food_list, 10 if len(food_list) > 10 else len(food_list))
        return select_food


def add(food, group_id):
    if not os.path.exists("recipe"):
        os.makedirs("recipe")
    rec_dir = "recipe/recipe_" + str(group_id) + ".txt"
    if not os.path.exists(rec_dir):
        with open(rec_dir, "a", encoding='utf-8') as f:
            pass
    with open(rec_dir, "r+", encoding='utf-8') as f:
        exist_food = f.read().split('\n')
        exist_food = list(filter(lambda x:x!='',exist_food))
        processed_food = []
        for fo in food:
            if len(fo) > 20:
                processed_food.append(fo[:20])
            else:
                processed_food.append(fo)
            if fo in exist_food:
                return {'code': 204, 'content': fo}
        for pfo in processed_food:
            print(exist_food)
            print(len(exist_food),processed_food.index(pfo))
            if len(exist_food) == 0 and processed_food.index(pfo) == 0:
                f.write(pfo)
            else:
                f.write('\n' + pfo)
        return {'code': 200, 'content': '\n'.join(processed_food),
                'rate': rate10_in_all(len(exist_food)) - rate10_in_all(len(exist_food) + len(processed_food))}


def get_count(group_id):
    if not os.path.exists("recipe"):
        os.makedirs("recipe")
    rec_dir = "recipe/recipe_" + str(group_id) + ".txt"
    if not os.path.exists(rec_dir):
        return [0, 0]
    with open(rec_dir, "r", encoding='utf-8') as f:
        food_list = f.read().split('\n')
        return [len(food_list), rate10_in_all(len(food_list))]


def get_story(foods):
    openai.api_base = "https://api.chatanywhere.tech/v1"
    openai.api_key = "sk-vUdoqlqdODGulzVxiJPBShCdHHxRKWI4gjq0zG1TANm3hR70"
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": "用以下十个词写一段一百字的中文故事:\n" + ",".join(foods),
            },
        ])
    return completion['choices'][0]['message']['content']


def rate10_in_all(n):
    return 100 * (1 - (comb(n - 1, 10) / comb(n, 10)))


def rate10_for_s_in_all(n, str_num):
    return 100 * (1 - (comb(n - str_num, 10) / comb(n, 10)))


def relate_count(food_str, group_id):
    if not os.path.exists("recipe"):
        os.makedirs("recipe")
    rec_dir = "recipe/recipe_" + str(group_id) + ".txt"
    if not os.path.exists(rec_dir):
        return [0, 0, 0]
    with open(rec_dir, "r", encoding='utf-8') as f:
        food_list = f.read().split('\n')
        re_count = 0
        for food in food_list:
            if food_str in food:
                re_count += 1
        return [re_count, len(food_list), rate10_for_s_in_all(len(food_list), re_count)]

def custom_requestGPT():
    api_key = "sk-vUdoqlqdODGulzVxiJPBShCdHHxRKWI4gjq0zG1TANm3hR70"
    url = "https://api.chatanywhere.tech/v1/chat/completions"
    header = {"Content-Type" : "application/json",
              "Authorization": f"Bearer {api_key}"}
    param = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {
            "role": "system",
            "content": "把下面的句子翻译成英文"
        },
        {
            "role": "user",
            "content": "你是谁"
        }
    ]}
    print(requests.post(url=url,data=json.dumps(param),headers=header).text)

custom_requestGPT()