import json
import os

import openai.error
from nonebot import get_driver, get_bot
from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment, MessageEvent, PRIVATE, GroupMessageEvent
from nonebot.internal.rule import Rule
from nonebot.params import CommandArg
from nonebot.plugin import on_command, on_endswith, on_startswith
from nonebot_plugin_apscheduler import scheduler
from .util import *

study_config = get_driver().config

tease_for_b50 = on_command("b50", priority=50)

@tease_for_b50.handle()
async def _tease_for_b50(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    await tease_for_b50.send(Message(MessageSegment.at(event.get_user_id)) + "又在查b50啦，杂鱼舞萌吃~")