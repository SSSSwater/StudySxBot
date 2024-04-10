import os

from nonebot import get_driver, get_bot
from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment, MessageEvent, PRIVATE, GroupMessageEvent
from nonebot.internal.rule import Rule
from nonebot.params import CommandArg
from nonebot.plugin import on_command, on_endswith, on_startswith

study_config = get_driver().config


word = on_command("word", priority=50)


@word.handle()
async def _word(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    with open("00022.png","rb") as f:
        msg = Message(MessageSegment.image(f.read()))
    await word.send(msg)
