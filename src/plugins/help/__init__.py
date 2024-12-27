import json
import os

from nonebot import get_driver, get_bot
from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment, MessageEvent, PRIVATE, GroupMessageEvent
from nonebot.internal.rule import Rule
from nonebot.params import CommandArg
from nonebot.plugin import on_command, on_endswith, on_startswith

study_config = get_driver().config

help = on_command("help", aliases=set(study_config.help_key), priority=50)

@help.handle()
async def _help(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    with open("help(qq).txt","r",encoding='utf-8') as f:
        await help.send(f.read())