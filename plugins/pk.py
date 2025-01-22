# -*- coding: utf-8 -*-
## 插件模板
from bilibili_api.user import User
from bilibili_api.live import LiveRoom
from bilibili_api import sync

from libs.user import c

api={}

def events(event:str):
    global roomcfg
    global send_msg
    roomcfg=api.get('roomcfg')
    send_msg=api.get('send_msg')
    if event['type'] in ['PK_BATTLE_PRE','PK_BATTLE_PRE_NEW']:
        pki=LiveRoom(event['data']['data']['room_id'],credential=c)
        users=User(event['data']['data']['uid'],credential=c)
        guards_num=sync(pki.get_dahanghai(1))['info']['num']
        follower=sync(users.get_relation_info())['follower']
        send_msg(text=f'pk主播:{event["data"]["data"]["uname"]} 粉丝数：{follower} 在舰数：{guards_num} ')
    return