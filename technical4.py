import numpy as np
import requests
import pandas as pd
from datetime import datetime
import json


def get_ohlcv(min,before=0,after=0):
    params={"periods" : min }
    if before != 0:
        params["before"]=before
    if after != 0:
        params["after"]=after
    res=requests.get("https://api.cryptowat.ch/markets/bitflyer/btcfxjpy/ohlc",params).json()['result'][str(min)]
    Time,Open,High,Low,Close,Volume=([],[],[],[],[],[])
    for i in res:
        Time.append(datetime.fromtimestamp(i[0]).strftime('%Y/%m/%d %H:%M'))
        Open.append(i[1])
        High.append(i[2])
        Low.append(i[3])
        Close.append(i[4])
        Volume.append(i[5])
    pd.DataFrame({'close':Close,'time':Time,'open':Open,'high':High,'low':Low,'volume':Volume}).to_csv('h4_4.csv')
    data=pd.read_csv("./h4_4.csv")
    return data
data=get_ohlcv(3600*4,0,1047888813)
#data=pd.read_csv("./h4_3.csv")
def cal_ma(para,data):
    MA=[]
    for i in range(len(data)):
        if i>para-2:
            ma=sum(data["close"][i-para+1:i+1])/para
            MA.append(ma)
        else:
            MA.append(0)
    return MA
#ma5=cal_ma(5)
#ma25=cal_ma(25)
#ma75=cal_ma(75)
#ma200=cal_ma(200)
def cal_macd(data):
    ma12=cal_ma(12)
    ma26=cal_ma(26)
    macd=[]
    signal=[]
    for i in range(len(data)):
        macd.append(ma12[i]-ma26[i])
    for i in range(8):
        signal.append(0)
    for i in range(len(data)-8):
        signal.append(sum(macd[i:i+8])/9)
    return macd,signal
#macd,signal=cal_macd()


def cal_iti(para1,para2,para3,data):
    iti1,iti2,iti3,iti4=([],[],[],[])
    for i in range(len(data)):
        if i < para1:
            iti1.append(0)
        else:
            kizyun=(max(data["high"][i-para1+1:i+1])+min(data["low"][i-para1+1:i+1]))/2
            iti1.append(kizyun)
        if i < para2:
            iti2.append(0)
        else:
            tenkan=(max(data["high"][i-para2+1:i+1])+min(data["low"][i-para2+1:i+1]))/2
            iti2.append(tenkan)
    for i in range(para2):
        iti3.append(0)
    for i in range(0,len(data)-para2):
        span1=(iti1[i]+iti2[i])/2
        iti3.append(span1)
    for i in range(para2+para3):
        iti4.append(0)
    for i in range(para3,len(data)-para2):
        span2=(max(data["high"][i-para3+1:i+1])+min(data["low"][i-para3+1:i+1]))/2
        iti4.append(span2)
    return iti1,iti2,iti3,iti4
#iti1,iti2,iti3,iti4=cal_iti(9,26,52)

def cal_boli(para,data):
    sigma1,sigma2,sigma_1,sigma_2=([],[],[],[])
    for i in range(len(data)):
        if i<para-1:
            sigma1.append(0)
            sigma2.append(0)
            sigma_1.append(0)
            sigma_2.append(0)
        else:
            ma=sum(data["close"][i-para+1:i+1])/para
            ma2_sum=sum(data["close"][i-para+1:i+1]**2)
            ma_sum2=ma*para**2
            sigma=(para*ma2_sum+ma_sum2)**0.5/(para*(para-1))
            sigma1.append(ma+sigma)
            sigma2.append(ma+sigma*2)
            sigma_1.append(ma+sigma*(-1))
            sigma_2.append(ma+sigma*(-2))
    return sigma1,sigma2,sigma_1,sigma_2
#sigma1,sigma2,sigma_1,sigma_2=cal_boli(25)

def cal_rsi(data):
    rsi=[]
    rsiup=[]
    rsidown=[]
    for i in range(15):
        rsi.append(0)
    for i in range(len(data)-15):
        price=data["close"][i:i+15]
        for v in range(14):
            dif=price[i+v+1]-price[i+v]
            if dif>0:
                rsiup.append(dif)
            else:rsidown.append(abs(dif))
        result=((sum(rsiup)/14)/(sum(rsiup)/14+sum(rsidown)/14))*100
        rsiup=[]
        rsidown=[]
        rsi.append(result)
    return rsi

def cal_stk(data):
    perK=[]
    perD=[]
    slowD=[]
    for i in range(9):
        perK.append(0)
    for i in range(len(data)-9):
        perK.append((data["close"][i+9]-min(data["low"][i:i+9]))/(max(data["high"][i:i+9])-min(data["low"][i:i+9])))
    for i in range(2):
        perD.append(0)
    for i in range(len(data)-2):
        perD.append(sum(perK[i:i+3])/3)
    for i in range(2):
        slowD.append(0)
    for i in range(len(data)-2):
        slowD.append(sum(perD[i:i+3])/3)
    return perK,perD,slowD
#perk,perd,slowd=cal_stk()

def cal_adx(data):
    dmup=[]
    dmdown=[]
    tr=[]
    diup=[]
    didown=[]
    dx=[]
    adx=[]
    for i in range(1):
        dmup.append(0)
        dmdown.append(0)
        tr.append(0)
    for i in range(len(data)-1):
        if data["high"][i+1]-data["high"][i]<0 and data["low"][i]-data["low"][i+1]:
            dmup.append(0)
            dmdown.append(0)
        elif data["high"][i+1]-data["high"][i]>data["low"][i]-data["low"][i+1]:
            dmup.append(data["high"][i+1]-data["high"][i])
            dmdown.append(0)
        else:
            dmdown.append(data["low"][i]-data["low"][i+1])
            dmup.append(0)
    for i in range(len(data)-1):
        if data["close"][i]<data["high"][i+1]:
            if data["close"][i]<data["low"][i+1]:
                tr.append(data["high"][i+1]-data["close"][i])
            else:tr.append(data["high"][i+1]-data["low"][i+1])
        else:
            if data["close"][i]>data["high"][i+1]:
                tr.append(data["close"][i]-data["low"][i+1])
            else:tr.append(data["high"][i+1]-data["low"][i+1])
    for i in range(13):
        diup.append(0)
        didown.append(0)
    for i in range(len(data)-13):
        diup.append((sum(dmup[i:i+14])/sum(tr[i:i+14]))*100)
        didown.append((sum(dmdown[i:i+14])/sum(tr[i:i+14]))*100)
    for i in range(len(data)):
        if diup[i]==0 and didown[i]==0:
            dx.append(0)
        else:dx.append((diup[i]-didown[i])/(diup[i]+didown[i]))
    for i in range(8):
        adx.append(0)
    for i in range(len(data)-8):
        adx.append(sum(dx[i:i+9])/9)
    return diup,didown,dx,adx

#diup,didown,dx,adx=cal_adx()

#pd.DataFrame({'time':Time,'open':Open,'high':High,'low':Low,'close':Close,'volume':Volume,"MA5":ma5,"MA25":ma25,"MA75":ma75,"MA200":ma200,"itimoku1":iti1,"itimoku2":iti2,"itimoku3":iti3,"itimoku4":iti4,"sigma1":sigma1,"sigma2":sigma2,"sigma_1":sigma_1,"sigma_2":sigma_2,"rsi":rsi}).to_csv('h4_3.csv')
#data2=pd.read_csv("./h4_3.csv")

#print(data2.tail())
