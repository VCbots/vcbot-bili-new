import os
import json
from loguru import logger
from dotenv import load_dotenv

default={
    'connected': '连接成功!', 
    'chat': {
        'global': {
            'schedule': [
                {'minute': 30, 'content': '主包记得喝水！'}, 
                {'minute': 15, 'content': '关注上舰送灯牌，寻找主包不迷路～'}
                ], 
            'events': {
                'reply_notice': ' {user} 回复 {re-user} : {content} ', 
                'welcome': '欢迎 {user} 进入直播间', 
                'gifts': '谢谢 {user} 的 {gift} 喵～', 
                'guard': '感谢 {user} 开通 {type} 喵～', 
                'followed': '感谢 {user} 的关注喵～'
                }, 
            'command': {
                '骂我':'杂鱼～杂鱼～'
                }
            },
        '282873551': {
            'command': {
                'debug': 'vcbot-bili with default rule'
                }
            }
        }
    }

def loadroomcfg():
    if not os.path.exists("./.env"):
        roomid=input("未检测到配置文件，请输入房间号:")
        term_login = "n"
        term_login = input("是否使用终端登录？(y/[n]):")
        if term_login.lower() == "y":
            term_env_set = 1
        else:
            term_env_set = 0
        with open("./.env",mode="w",encoding="utf-8",errors="ignore") as env:
            env.write(f"roomid={roomid}\nterm_env={term_env_set}")
    load_dotenv(dotenv_path="./.env")
    global room
    room=os.environ["roomid"]
    global term_env
    term_env = os.environ["term_env"]
    global roomcfg
    global plugins_cfg
    try:
        roomcfg = json.load(open(f"./{room}.json",encoding="utf-8",errors="ignore"))
    except FileNotFoundError:
        roomcfg = default.copy()
        _make_default_cfg()
    finally:
        logger.info(str(roomcfg))
    return

def _make_default_cfg():
    with open(file=f"./{room}.json",mode="w",encoding="utf-8",errors="ignore") as cookies:
        cookies.write(json.dumps(default,ensure_ascii=False))
            
if __name__ == "__main__":
    #方便转换，直接运行这个py文件
    roomcfg = json.load(open("example.json",encoding="utf-8",errors="ignore"))
    print(roomcfg)
    with open('dist.txt',encoding='utf-8',errors='ignore',mode='w') as dists:
        dists.write(str(roomcfg))