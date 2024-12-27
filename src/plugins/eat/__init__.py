import json
import os

import openai.error
from nonebot import get_driver, get_bot
# from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment, MessageEvent, PRIVATE, GroupMessageEvent
from nonebot.adapters.qq import Bot,Message,MessageEvent,Event
from nonebot.internal.rule import Rule
from nonebot.params import CommandArg
from nonebot.plugin import on_command, on_endswith, on_startswith
from nonebot_plugin_apscheduler import scheduler
from .util import *

study_config = get_driver().config

eat = on_command("eat", aliases=set(study_config.eat_key), priority=50)
add_food = on_command("add_food", aliases=set(study_config.add_key), priority=50)
count = on_command("count", aliases=set(study_config.count_key), priority=50)
re_count = on_command("re_count", aliases=set(study_config.re_count_key), priority=50)

@eat.handle()
async def _eat(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    print("收到消息:",bot,event)
    await bot.send(event, "测试")
    get_food = random_10(event.group_id)
    msg = "给群友上了这些菜:"
    i = 1
    for food in get_food:
        msg += ("\n第" + str(i) + "道菜:" + food)
        i += 1
    msg += "\n祝用餐愉快~"
    try:
        story = get_story(get_food)
        msg += "\n\n以下是一则小故事~\n" + story
    except openai.error.RateLimitError as e:
        msg += "\n\n今日100次小故事机会用完啦，暂时无法使用故事模块，请等待第二天刷新~"
    except Exception as e:
        msg += str(e)

    await eat.send(msg)


@add_food.handle()
async def _add(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    food = args.extract_plain_text()
    response = add(food.split('\n'),event.group_id)
    status = response['code']
    if status == 200:
        await add_food.send(response['content'] + "\n添加成功喵\n你为词库降低了" + str(response['rate']) + "%的出货率~")
    elif status == 204:
        await add_food.send("添加失败\n" + response['content'] + "已存在")
    else:
        await add_food("添加失败")


@count.handle()
async def _count(event: MessageEvent):
    res = get_count(event.group_id)
    await count.send("目前菜谱中已有" + str(res[0]) + "道菜!\n抽到你想要的某个菜的概率为:" + str(res[1]) + "%~")


@re_count.handle()
async def _re_count(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    food = args.extract_plain_text()
    res = relate_count(food,event.group_id)
    await re_count.send("目前菜谱中包含" + food + "的数量为:" + str(res[0]) + "/" + str(res[1]) + "\n抽到相关菜的概率为:" + str(res[2]) + "%~")
