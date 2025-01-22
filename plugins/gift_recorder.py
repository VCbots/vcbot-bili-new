'''
礼物数据记录
'''
import os
import datetime
import csv

from loguru import logger

api={}
header=['时间','UID','用户名','礼物名','数量','价格']
header_blind=['时间','UID','用户名','盲盒名称','盲盒价格（单价）','礼物名','数量','实际礼物价格(单价)','盈亏（总价）']


if os.path.exists('data')==False:
    os.mkdir('data')
if os.path.exists('data/gift-'+str(datetime.date.today())+'.csv')==False:
    with open(f'data/gift-{datetime.date.today()}.csv','a',newline='',encoding='utf-8-sig') as f:
        writer=csv.writer(f)
        writer.writerow(header)
if os.path.exists('data/gift-'+str(datetime.date.today())+'-blind.csv')==False:
    with open(f'data/gift-{datetime.date.today()}-blind.csv','a',newline='',encoding='utf-8-sig') as f:
        writer=csv.writer(f)
        writer.writerow(header_blind)
    
def save(data:dict):
    data=data['data']['data']
    today=datetime.date.today()
    timestamp=datetime.datetime.fromtimestamp(data['timestamp'])
    timestamp=timestamp.strftime('%Y-%m-%d %H:%M:%S')
    with open(f'data/gift-{today}.csv','a',newline='',encoding='utf-8-sig') as f:
        writer=csv.writer(f)
        writer.writerow([timestamp,data['uid'],data['uname'],data['giftName'],data['num'],f"{int(data['price'])/1000}元"])

def save_for_blind_gift(data:dict):
    data=data['data']['data']
    blind=data['blind_gift']
    origin_gift=blind['original_gift_name']
    price=int(blind['original_gift_price'])/1000 #int后转成金额
    gift_price=int(blind['gift_tip_price'])/1000 #int后转成金额
    totals=(gift_price - price) * int(data['num'])
    timestamp=datetime.datetime.fromtimestamp(data['timestamp'])
    timestamp=timestamp.strftime('%Y-%m-%d %H:%M:%S')
    today=datetime.date.today()
    with open(f'data/gift-{today}-blind.csv','a',newline='',encoding='utf-8-sig') as f:
        writer=csv.writer(f)
        writer.writerow([timestamp,data['uid'],data['uname'],origin_gift,f"{price}元",data['giftName'],data['num'],f"{gift_price}元",f"{totals}元"])
        
def check_blind(event:str):
    try:
        blind=event['data']['data']['blind_gift']
    except TypeError:
        return False
    if blind==None:
        return False
    return True
    

def events(event:str):
    global roomcfg
    global send_msg
    roomcfg=api.get('roomcfg')
    send_msg=api.get('send_msg')
    event_type=event["type"]
    if event_type=="SEND_GIFT":
        if check_blind(event):
            save_for_blind_gift(event)
            return
        else:
            save(event)
            return
    return