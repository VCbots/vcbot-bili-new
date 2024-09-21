from loguru import logger
from apscheduler.schedulers.blocking import BlockingScheduler
from bilibili_api import sync
from . import config,live

api={}
Timer=BlockingScheduler()
def schedule_ctrl(min:int=None,arg:str=None):
    sec=min*60
    logger.debug(str(min)+"min "+str(arg))
    Timer.add_job(schedule_run,trigger='interval',seconds=sec,args=[arg])
    return

def schedule_run(text:str):
    logger.debug(text)
    try:
        sync(live.send_danmu(text=text))
    except:
        logger.warning("schedule error!")
    return

def close():
    Timer.shutdown(False)

def start():
    try:
        cfg = config.roomcfg['chat']['global']['schedule']
    except:
        return
    n= len(cfg)
    for i in range(0,n,1):
        schedule_ctrl(int(cfg[i]['minute']),str(cfg[i]['content']))
    Timer.start()
    return

def events(event:str):
    global send_msg
    global roomcfg
    send_msg=api.get("send_msg")
    roomcfg=api.get("roomcfg")

