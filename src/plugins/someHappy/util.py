import os
import random
import time

hair_list=["绿","黄","黑","红","棕","蓝","粉","白","紫"]

def get_today_time():
    return str(time.localtime().tm_year.real) + "0" + str(time.localtime().tm_mon.real) + "0" + str(
        time.localtime().tm_mday.real)


def today_oc(qq):
    if not os.path.exists("oc"):
        os.makedirs("oc")
    oc_dir = "oc/" + str(qq) + get_today_time() + ".txt"
    if not os.path.exists(oc_dir):
        hair = random.sample(hair_list, 1)[0]
        sex = random.randint(1, 3)
        hp = random.randint(80, 100)
        attk = random.randint(10, 15)
        defs = random.randint(7, 10)
        lg = random.randint(5, 8)
        with open(oc_dir, "a", encoding='utf-8') as f:
            pass
        with open(oc_dir, "w", encoding='utf-8') as f:
            f.write(str(sex) + "\n" + str(hp) + "\n" + str(attk) + "\n" + str(defs) + "\n" + str(lg))
        return {'status': 200, 'content': [sex, hp, attk, defs, lg]}
    else:
        with open(oc_dir, "r", encoding='utf-8') as f:
            stats = f.read().split('\n')
        return {'status': 204,'content': [int(x) for x in stats]}

print(today_oc(307722647))