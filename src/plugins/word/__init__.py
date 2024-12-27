import json
import os

from nonebot import get_driver, get_bot
from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment, MessageEvent, PRIVATE, GroupMessageEvent
from nonebot.internal.rule import Rule
from nonebot.params import CommandArg
from nonebot.plugin import on_command, on_endswith, on_startswith
from nonebot_plugin_apscheduler import scheduler
from .word_util import *

study_config = get_driver().config
group_list = study_config.dict()["word_group"]


# 群权限
async def group_rule(event: GroupMessageEvent):
    if str(event.group_id.real) in group_list:
        return True
    else:
        return False


word = on_command("word", permission=group_rule | PRIVATE, priority=50)


@word.handle()
async def _word(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    get_word = random_word()
    get_sentence = random.randint(0, len(get_word['sentences']) - 1)
    msg = "抽到单词如下:\n" + get_word['word'] + " " + get_word['usphone'] + "\n释义:"
    for tr in get_word['translates']:
        msg += ("\n" + tr['position'] + ". " + tr['tranCn'])
    msg += ("\n随机例句:\n" + get_word['sentences'][get_sentence]['sContent'] + "\n释义:\n" +
            get_word['sentences'][get_sentence]['sCn'])
    await word.send(msg)


async def word_everyday():
    for g in group_list:
        get_word = random_word()
        get_sentence = random.randint(0, len(get_word['sentences']) - 1)
        msg = "今日零点单词!\n" + get_word['word'] + " " + get_word['usphone'] + "\n释义:"
        for tr in get_word['translates']:
            msg += ("\n" + tr['position'] + ". " + tr['tranCn'])
        msg += ("\n随机例句:\n" + get_word['sentences'][get_sentence]['sContent'] + "\n释义:\n" +
                get_word['sentences'][get_sentence]['sCn'])
        await get_bot().send_group_msg(group_id=g, message=msg)

scheduler.add_job(word_everyday, "cron", hour="0", minute="0", id="word_everyday")
