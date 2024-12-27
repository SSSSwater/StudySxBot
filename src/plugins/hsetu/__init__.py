from nonebot import get_driver, get_bot
from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment, MessageEvent, PRIVATE, GroupMessageEvent
from nonebot.internal.rule import Rule
from nonebot.params import CommandArg, T_State
from nonebot.plugin import on_command, on_endswith, on_startswith

from .api_utils import *

study_config = get_driver().config


# 群权限
async def group_rule(event: GroupMessageEvent):
    group_list = study_config.dict()["h_group"]
    if str(event.group_id.real) in group_list:
        return True
    else:
        return False


H = on_command("H", permission=group_rule | PRIVATE, priority=50)
myH = on_command("myH", permission=group_rule | PRIVATE, priority=50)
H_post = on_command("H_post", permission=group_rule | PRIVATE, priority=60)

status_code_dict = {
    200: "获取成功", 201: "提交成功", 204: "账号已存在", 401: "请先注册", 404: "未找到"
}


@H.handle()
async def _H(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    response = get_H()
    status_code = response.status_code
    '''
    {'qq': './uploads/1821605260/_$(c]k$~KFd_ziu65c4Q}4Lr5YZ}L1Y.jpeg',
     'date': 'Sun, 19 May 2024 07:03:38 GMT'}
    '''
    from_id = response.headers['qq'].split('/')[2]
    if status_code == 200:
        await H.send(MessageSegment.image(response.content) + MessageSegment.text(
            "\n来自" + get_nickname(from_id) + "(" + from_id + ")的图图~"))
    elif status_code == 404:
        await H.send("还未上传过图片哦~H杂鱼~")
    else:
        await H.send("未知错误(" + str(status_code) + ")")


@myH.handle()
async def _H(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    response = get_H(event.get_user_id())
    status_code = response.status_code
    if status_code == 200:
        await H.send(MessageSegment.image(response.content) + MessageSegment.text(
            "\n来自你自己的图图~"))
    elif status_code == 404:
        await H.send("你还未上传过图片哦~H杂鱼~")
    else:
        await H.send("未知错误(" + str(status_code) + ")")


@H_post.handle()
async def _H_post_cmd(bot: Bot, event: MessageEvent, state: T_State, args: Message = CommandArg()):
    print(args)
    state['id'] = event.get_user_id()
    for a in args:
        print(a)
        if a.type == "image":
            state['img'] = Message(a)
            break


@H_post.got("img", prompt="请发送图片哦")
async def _H_post_img(event: MessageEvent, state: T_State):
    print(state)
    for seg in state["img"]:
        if seg.type == "image":
            response = post_H(seg.data['url'], event.get_user_id())
            status = response['code']
            if status == 200:
                await H_post.send(Message(MessageSegment.at(state['id'])) + "上传成功")
            else:
                await H_post.send(Message(MessageSegment.at(state['id'])) + "上传失败(" + str(status) + ")," + response['msg'])
            break
