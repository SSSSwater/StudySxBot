from nonebot import get_driver, get_bot
from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment, MessageEvent, PRIVATE, GroupMessageEvent
from nonebot.internal.rule import Rule
from nonebot.params import CommandArg
from nonebot.plugin import on_command

from .api_utils import *

study_config = get_driver().config


# 群权限
async def group_rule(event: GroupMessageEvent):
    group_list = study_config.dict()["study_group"]
    if str(event.group_id.real) in group_list:
        return True
    else:
        return False


H = on_command("H", aliases=set(study_config.h_key), permission=group_rule | PRIVATE, priority=50)

status_code_dict = {
    200: "获取成功", 201: "提交成功", 204: "账号已存在", 401: "请先注册", 404: "未找到"
}


@H.handle()
async def _H(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    await H.send(MessageSegment.image(get_H().content))
