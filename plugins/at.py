import json

api={}

def events(event:str):
    global roomcfg
    global send_msg
    roomcfg=api.get('roomcfg')
    send_msg=api.get('send_msg')
    if event['type']=='DANMU_MSG':
        if check_at(event):
            send_at_notice(event=event)
            raise api.get('exception')("at")
def check_at(event:str):
    extra=event['data']['info'][0][15]['extra']
    jsond=json.loads(extra)
    print(jsond['reply_uname'])
    if str(jsond['reply_uname']) == '' or None:
        return False
    else:
        return True
    
def send_at_notice(event:str):
    model = str(roomcfg['chat']['global']['events']['reply_notice'])
    extra=event['data']['info'][0][15]['extra']
    jsond=json.loads(extra)
    uname=event['data']['info'][2][1]
    r_uname=jsond['reply_uname']
    text=event['data']['info'][1]
    content_user=model.replace(' {user} ',f'{uname} ')
    content_ruser=content_user.replace(' {re-user} ',f'@{r_uname} ')
    contented=content_ruser.replace(' {content} ',f'{text}')
    send_msg(text=contented)