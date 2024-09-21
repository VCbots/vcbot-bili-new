import os
import json
import datetime
import threading
import importlib.util

from loguru import logger
from bilibili_api import sync
from libs import live,user,config,ignore
from libs import inital_command,schedule

skip=False
def load_config():
    global vcbot_api
    vcbot_api={"send_msg": send_msgs ,"exception": vcbot_plugin_DoNotContinue,"ban_uid":ignore.ban_uid}
    config.loadroomcfg()
    vcbot_api["roomcfg"]=config.roomcfg
    botuid=user.get_self_uid(user.c)
    vcbot_api["bot_uid"]=botuid
def load_plugin():
    for file in os.listdir("plugins"):
        if file.endswith(".py") and file!="__init__.py":
            logger.info(f"Loading plugin {file}")
            spec = importlib.util.spec_from_file_location(f"plugins.{file[:-3]}", f"plugins/{file}")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.api = vcbot_api.copy()
@logger.catch
async def plugins_event(event:str): # event:all
    skip=False
    for file in os.listdir("plugins"):
        if file.endswith(".py") and file!="__init__.py":
            # 调用定义为events的函数
            try:
                module = importlib.import_module(f"plugins.{file[:-3]}")
                module.api=vcbot_api.copy()
                threading.Thread(target=module.events, args=(event,)).start()
                threading.Thread(target=schedule.events, args=(event,)).join()
            except AttributeError:
                pass
            except vcbot_plugin_DoNotContinue: 
                skip=True
                break
            except Exception as e:
                logger.error(f"Error in plugin {file}: {e}")
                raise
    if not skip:
        inital_command.api=vcbot_api.copy()
        threading.Thread(target=inital_command.events, args=(event,)).start()
        threading.Thread(target=schedule.events, args=(event,)).join()
    return 

def send_msgs(text:str):
    logger.info(f'send:{text}')
    sync(live.send_danmu(text))


def listen():
    @live.LiveDanma.on("ALL")
    async def event(event:str):
        logger.debug(f'收到事件：\n{json.dumps(event,ensure_ascii=False)}')
        await plugins_event(event)
        return
    logger.info("开始监听")
    print(vcbot_api)
    try:
        sync(live.LiveDanma.connect())
    finally:
        sync(live.LiveDanma.disconnect())
        schedule.close()
        os._exit(0)

class vcbot_plugin_DoNotContinue(Exception):
    def __init__(self,msg:str=None):
        self.msg=msg
        skip=True

if __name__ == '__main__':
    logger.info("Starting...")
    today=datetime.date.today()
    logger.add(f"logs/log-{today}.log",rotation="1 day",encoding="utf-8",format="{time} {level}-{function} {message}")
    user.user_login()
    load_config()
    live.set(config.room,user.c)
    load_plugin()
    threading.Thread(target=schedule.start).start()
    listen()