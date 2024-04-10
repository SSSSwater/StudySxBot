import random
import re
import time
from datetime import datetime

from apscheduler.jobstores.base import ConflictingIdError, JobLookupError
from nonebot import get_driver, get_bot
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message, MessageSegment, MessageEvent, \
    PRIVATE
from nonebot.internal.rule import Rule
from nonebot.params import CommandArg
from nonebot.plugin import on_command
from nonebot_plugin_apscheduler import scheduler

from .api_utils import *

study_config = get_driver().config


# 群权限
async def group_rule(event: GroupMessageEvent):
    group_list = study_config.dict()["study_group"]
    if str(event.group_id.real) in group_list:
        return True
    else:
        return False


test = on_command("test", aliases=set(study_config.test_key), permission=group_rule | PRIVATE, priority=50)
daka = on_command("daka", aliases=set(study_config.daka_key), permission=group_rule | PRIVATE, priority=50)
reg = on_command("reg", aliases=set(study_config.reg_key), permission=group_rule | PRIVATE, priority=50)
reg_list = on_command("reg_list", aliases=set(study_config.reg_list_key), permission=group_rule | PRIVATE, priority=50)
modify_name = on_command("modify_name", aliases=set(study_config.modify_name_key), permission=group_rule | PRIVATE,
                         priority=50)
today_list = on_command("today_list", aliases=set(study_config.today_list_key), permission=group_rule | PRIVATE,
                        priority=50)
remind_once = on_command("remind_once", aliases=set(study_config.remind_once_key), permission=group_rule | PRIVATE,
                         priority=50)
remind_once_cancel = on_command("remind_once_cancel", aliases=set(study_config.remind_once_cancel_key),
                                permission=group_rule | PRIVATE, priority=50)
remind_routine_set = on_command("remind_routine_set", aliases=set(study_config.remind_routine_set_key),
                                permission=group_rule | PRIVATE, priority=50)
remind_routine_manual = on_command("remind_routine_manual", aliases=set(study_config.remind_routine_manual_key),
                                   permission=group_rule | PRIVATE,
                                   priority=50)
remind_summary_manual = on_command("remind_summary_manual", aliases=set(study_config.remind_summary_manual_key),
                                   permission=group_rule | PRIVATE,
                                   priority=50)
remind_routine_cancel = on_command("remind_routine_cancel", aliases=set(study_config.remind_routine_cancel_key),
                                   permission=group_rule | PRIVATE,
                                   priority=50)

status_code_dict = {
    200: "获取成功", 201: "提交成功", 204: "账号已存在", 401: "请先注册", 404: "未找到"
}


@daka.handle()
async def _daka(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    word_num = 0
    pic_url = None
    for a in args:
        if a.type == "image":
            pic_url = a.data['url']
        elif a.type == "text":
            word_num = a.data['text'].strip()
    if not pic_url:
        await attempt_send(bot, event, "请打卡的同时发送截图当作打卡证明喵")
        await daka.finish()
    response = post_daka(event.get_user_id(), pic_url, word_num)
    status = response.status_code
    if status == 201:
        text_list = study_config.dict()["daka_tail"]
        await attempt_send(bot, event, "成功打卡!\n背了" + str(word_num) + "个单词，" + text_list[
            random.randint(0, len(text_list) - 1)])
    elif status == 204:
        await attempt_send(bot, event, "不要重复打卡")
    elif status == 401:
        await attempt_send(bot, event, "请先注册")
    else:
        await attempt_send(bot, event, "打卡失败(" + str(status) + ")")


@reg.handle()
async def _reg(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    name = args.extract_plain_text()
    qq = event.get_user_id()
    if name:
        response = post_register(qq, name)
        status = response.status_code
        if status == 201:
            post_remind_list(qq, "22")
            await attempt_send(bot, event, name + "(" + qq + ")注册成功，已自动设置打卡提醒为22:00")
        elif status == 204:
            await attempt_send(bot, event, "重复注册")
        else:
            await attempt_send(bot, event, "注册失败(" + str(status) + ")")
    else:
        await attempt_send(bot, event, "请输入注册昵称喵")


@reg_list.handle()
async def _reg_list(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    response = get_register()
    status = response.status_code
    if status == 200:
        message = "打卡名单:"
        regs = response.json()
        for r in regs:
            message += ("\n" + r['name'] + "(" + r['qq'] + ")")
        await attempt_send(bot, event, message)
    else:
        await attempt_send(bot, event, "获取失败(" + int(status) + ")")


@modify_name.handle()
async def _modify_name(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    name = args.extract_plain_text()
    qq = event.get_user_id()
    if name:
        response = put_register(qq, name)
        status = response.status_code
        if status == 204:
            await attempt_send(bot, event, name + "(" + qq + ")修改昵称成功")
        else:
            await attempt_send(bot, event, "修改失败(" + str(status) + ")")
    else:
        await attempt_send(bot, event, "请输入修改昵称喵")


@today_list.handle()
async def _today_list(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    message = Message([MessageSegment.text("今日打卡情况:\n已打卡:\n")])
    response = get_today_list()
    status = response.status_code
    if status == 200:
        for d in response.json():
            message += (d['name'] + "(" + d['qq'] + ") 单词数:" + str(d['word_num']) + "\n")
        message += ("共计" + str(len(response.json())) + "人已打卡\n")

    else:
        message += ("获取失败(" + str(status) + ")")
    message += "\n未打卡:\n"
    response = get_death_list()
    status = response.status_code
    if status == 200:
        for d in response.json():
            message += (d['name'] + "(" + d['qq'] + ")\n")
        message += ("共计" + str(len(response.json())) + "人未打卡")
    else:
        message += ("获取失败(" + str(status) + ")")
    await attempt_send(bot, event, message)


@remind_once.handle()
async def _remind_once(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    remind_args = args.extract_plain_text().split(' ')
    if len(remind_args) > 2:
        msg = "该" + remind_args[2] + "了少爷"
    else:
        msg = "提醒时间到"
    try:
        local_time = time.localtime()
        scheduler.add_job(attempt_send, "date",
                          kwargs={"bot": bot, "event": event, "msg": msg, "to_me": True},
                          run_date=datetime(local_time.tm_year.real,
                                            local_time.tm_mon.real,
                                            local_time.tm_mday.real,
                                            int(remind_args[0]),
                                            int(remind_args[1]),
                                            0),
                          id="once_" + event.get_user_id())
        await attempt_send(bot, event, "已设置" + str(remind_args[0]).rjust(2, '0') + ":" + str(remind_args[1]).rjust(2,
                                                                                                                   '0') + "提醒你" + (
                               remind_args[2] if len(remind_args) > 2 else ""))
    except ConflictingIdError:
        await attempt_send(bot, event, "你已设置提醒事件，若需设置其他提醒请先取消当前提醒(/remind_c)")


@remind_once_cancel.handle()
async def _remind_once_cancel(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    try:
        scheduler.remove_job("once_" + event.get_user_id())
        await attempt_send(bot, event, "已取消当前提醒事件")
    except JobLookupError:
        await attempt_send(bot, event, "当前没有进行中的提醒事件")


@remind_routine_set.handle()
async def _remind_routine_set(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    remind_args = args.extract_plain_text().split(' ')
    qq = event.get_user_id()
    set_time = remind_args[0]
    if not re.match("^([0-9]|[0-1][0-9]|2[0-3])$", string=set_time):
        await attempt_send(bot, event, "请输入0-23的整数!")
        await remind_routine_set.finish()
    response = post_remind_list(qq, str(set_time).rjust(2, '0'))
    status = response.status_code
    if status == 201:
        await attempt_send(bot, event, "已设置每日打卡提醒为" + str(set_time).rjust(2, '0') + ":00")
    elif status == 204:
        response_put = put_remind_list(qq, str(set_time).rjust(2, '0'))
        status_put = response_put.status_code
        if status_put == 204:
            await attempt_send(bot, event, "已修改每日打卡提醒为" + str(set_time).rjust(2, '0') + ":00")
        else:
            await attempt_send(bot, event, "修改失败(" + str(status_put) + ")")
    elif status == 401:
        await attempt_send(bot, event, "请先注册")
    else:
        await attempt_send(bot, event, "设置失败(" + str(status) + ")")


@remind_routine_cancel.handle()
async def _remind_routine_cancel(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    response = delete_remind_list(event.get_user_id())
    status = response.status_code
    if status == 204:
        await attempt_send(bot, event, "已关闭打卡提醒")
    elif status == 404:
        await attempt_send(bot, event, "你还未设置提醒或未注册")
    else:
        await attempt_send(bot, event, "关闭失败(" + str(status) + ")")


# 尝试群消息，若风控则私聊回复
async def attempt_send(bot: Bot,
                       event: MessageEvent,
                       msg: str,
                       to_me: bool = False):
    try:
        if to_me:
            msg = MessageSegment.at(event.get_user_id()) + msg
        await bot.send(event=event, message=msg)
    except:
        await bot.send_private_msg(user_id=event.get_user_id(), message=msg)


# 到设定的时间点调用，若未打卡进行提醒
async def routine_remind():
    current_hour = time.localtime().tm_hour.real
    remind_time_list = get_remind_list().json()
    now_to_remind_list = []
    for r in remind_time_list:
        if int(r['time']) == current_hour:
            now_to_remind_list.append(r['qq'])
    current_death_list = get_death_list(0).json()
    real_to_remind_list = []
    for i in now_to_remind_list:
        if i in [d['qq'] for d in current_death_list]:
            real_to_remind_list.append(i)
    for q in real_to_remind_list:
        await get_bot().send_private_msg(user_id=q, message=str(
            current_hour) + "点了，今天还你还没背单词哦，该背单词了\n(若想更改每日提醒时间可用 /routine xx[0-23] )")


# 手动提醒
@remind_routine_manual.handle()
async def routine_remind_manual():
    current_hour = time.localtime().tm_hour.real
    current_death_list = get_death_list(0).json()
    real_to_remind_list = []
    for i in current_death_list:
        real_to_remind_list.append(i['qq'])
    for q in real_to_remind_list:
        await get_bot().send_private_msg(user_id=q, message=str(
            current_hour) + "点了，今天还你还没背单词哦，该背单词了\n(若想更改每日提醒时间可用 /routine xx[0-23] )")


# 到6点调用，总结前一天打卡情况
@remind_summary_manual.handle()
async def routine_summary():
    marked_list: list = get_today_list(1).json()
    unmarked_list: list = get_death_list(1).json()

    message = Message([MessageSegment.at("all")])
    message += (
        MessageSegment.text("\n昨日打卡情况:\n" + str(len(marked_list)) + "人已打卡 " + str(len(unmarked_list)) + "人未打卡\n"))
    if len(unmarked_list) == 0:
        message += "所有人完成了打卡!\n"
    else:
        message += "未打卡名单为:\n"
        for l in unmarked_list:
            message += (l['name'] + "(" + l['qq'] + ")\n")
        message += "对以上同学狠狠批判!七宗罪的懒惰让你们犯了七遍!\n"
    message += "\n昨日打卡最早的人是:\n"
    earliest = marked_list[0]
    message += MessageSegment.image(earliest['pic_url'])
    message += (earliest['name'] + "(" + earliest['qq'] + ")，竟然在" + earliest['time'].split(' ')[
        1] + "就完成了打卡!\n昨日单词最多的人是:\n")

    marked_list.sort(key=lambda x: x['word_num'], reverse=True)
    most = marked_list[0]
    message += MessageSegment.image(most['pic_url'])
    message += (most['name'] + "(" + most['qq'] + ")，竟然背了" + str(most['word_num']) + "个单词")
    await get_bot().send_group_msg(group_id=study_config.remind_routine_group, message=message)


# 测试整点提醒
async def test_routine():
    marked_list: list = get_today_list(1).json()
    unmarked_list: list = get_death_list(1).json()
    message = Message(
        [MessageSegment.text("昨日打卡情况:\n" + str(len(marked_list)) + "人已打卡 " + str(len(unmarked_list)) + "人未打卡\n")])
    if len(unmarked_list) == 0:
        message += "所有人完成了打卡!\n"
    else:
        message += "未打卡名单为:\n"
        for l in unmarked_list:
            message += (l['name'] + "(" + l['qq'] + ")\n")
        message += "对以上同学狠狠批判!七宗罪的懒惰让你们犯了七遍!\n"
    message += "\n昨日打卡最早的人是:\n"
    earliest = marked_list[0]
    message += MessageSegment.image(earliest['pic_url'])
    message += (earliest['name'] + "(" + earliest['qq'] + ")，竟然在" + earliest['time'].split(' ')[
        1] + "就完成了打卡!\n昨日单词最多的人是:\n")

    marked_list.sort(key=lambda x: x['word_num'], reverse=True)
    most = marked_list[0]
    message += MessageSegment.image(most['pic_url'])
    message += (most['name'] + "(" + most['qq'] + ")，竟然背了" + str(most['word_num']) + "个单词")
    await get_bot().send_private_msg(user_id=307722647, message=str(time.localtime().tm_hour.real) + ":" + str(
        time.localtime().tm_min.real) + "\n" + message)


# 测试
@test.handle()
async def _test():
    await get_bot().send_group_msg(group_id="961471314", message=MessageSegment.at("all"))


scheduler.add_job(routine_remind, "cron", hour="*", minute="1", id="routine")
# scheduler.add_job(test_routine, "cron", hour="*", id="routine_test")
scheduler.add_job(routine_summary, "cron", hour="8", id="routine_s")