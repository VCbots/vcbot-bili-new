# -*- coding: utf-8 -*-
## 插件模板

api={}

def events(event:str):
    global roomcfg
    global send_msg
    roomcfg=api.get('roomcfg')
    send_msg=api.get('send_msg')
    print(event)
    return