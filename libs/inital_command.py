from bilibili_api import sync
from loguru import logger
from . import config,live,ignore

api={}
def get_danmaku_content(event:str):
    uid=event["data"]["info"][2][0]
    content=event["data"]["info"][1]
    if str(uid) == api.get("bot_uid"):
        return ""
    logger.info(content)
    try:
        contents=roomcfg["chat"][f"{uid}"]["command"][content]
    except:
        try:
            contents=roomcfg["chat"]["global"]["command"][content]
            logger.info("Reply:"+str(contents))
        except KeyError as e:
            return ""
    return contents

def get_danmaku_on_gift(event:str):
    info = event['data']['data']
    giftname=info['giftName']
    name= info['uname']
    try:
        contents=str(roomcfg["chat"]["global"]["events"]['gifts'])
        content_name=contents.replace(" {user} ",f"{name}")
        contented=content_name.replace(" {gift} ",f"{giftname}")
    except:
        logger.info("Reply:"+str(contented))
    return contented

def get_danmaku_on_wuser(event:str):
    info = event['data']['data']
    name= info['uname']
    if str(info['uid']) in ignore.ban_uid:
        return
    elif str(info['uid']) in live.owner_uid:
        return
    elif name.startswith("bili_"):
        return
    elif info['is_spread']!=0:
        return
    try:
        contents=str(roomcfg["chat"]["global"]["events"]['welcome'])
        content_name=contents.replace(" {user} ",f"{name}")
    except:
        logger.info("reply:"+str(content_name))
    return content_name

def get_danmaku_on_buyguard(event:str):
    info = event['data']['data']
    print(info)
    giftname=info['gift_name']
    name= info['username']
    num= info['num']
    try:
        contents=str(roomcfg["chat"]["global"]["events"]['guard'])
        content_name=contents.replace(" {user} ",f"{name}")
        content_num=content_name.replace(" {type} ",f"{giftname}")
        contented=content_num.replace(" {num} ",f"{num}")
    except:
        logger.info("Reply:"+str(contented))
    return contented

def get_danmaku_on_user_followed(event:str):
    print(event)
    info = event['data']['data']
    name= info['uname']
    try:
        contents=str(roomcfg["chat"]["global"]["events"]['followed'])
        content_name=contents.replace(" {user} ",f"{name}")
    except:
        logger.info("reply:"+str(content_name))
    return content_name

def _get_guard_type(num:int):
    if num == 1:
        return "总督"
    if num == 2:
        return "提督"
    if num == 3:
        return "舰长"

def events(event:dict):
    global roomcfg
    roomcfg=config.roomcfg.copy()
    event_type=event["type"]
    if event_type=="VERIFICATION_SUCCESSFUL":
        logger.info("Login Successful")
        send_msg(roomcfg['connected'])
        return
    if event_type=="DANMU_MSG":
        content=get_danmaku_content(event)
        if content!="":
            send_msg(content)
            logger.info("Reply:"+str(content))
            return True
        return False
    if event_type=="SEND_GIFT":
        content=get_danmaku_on_gift(event)
        if content!="":
            send_msg(content)
            logger.info("Reply:"+str(content))
            return True
        return False
    if event_type=="INTERACT_WORD":
        if event["data"]["data"]["msg_type"] ==1:
            content=get_danmaku_on_wuser(event)
            if content!="":
                send_msg(content)
                logger.info("Reply:"+str(content))
                return True
            return False             
        if event["data"]["data"]["msg_type"] ==2:
            content=get_danmaku_on_user_followed(event)
            if content!="":
                send_msg(content)
                logger.info("Reply:"+str(content))
                return True
            return False
        return False
    if event_type=="GUARD_BUY":
        content=get_danmaku_on_buyguard(event)
        if content!="":
            send_msg(content)
            logger.info("Reply:"+str(content))
            return True
        return False
    
def send_msg(text:str):
    sync(live.send_danmu(text))