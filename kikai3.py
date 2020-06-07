import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
import warnings
from sklearn import linear_model
from technical4 import get_ohlcv,cal_ma,cal_iti,cal_boli,cal_rsi,cal_stk,cal_macd,cal_adx

def dataset():
    #data=get_ohlcv(3600*4,0,1050567213)
    data=pd.read_csv("./h4_4.csv")
    #data["ma5"]=cal_ma(5)
    #data["ma25"]=cal_ma(25)
    #data["ma75"]=cal_ma(75)
    #data["ma200"]=cal_ma(200)
    #data["iti1"],data["iti2"],data["iti3"],data["iti4"]=cal_iti(9,26,52)
    #data["sigma1"],data["sigma2"],data["sigma_1"],data["sigma_2"]=cal_boli(25)
    data["rsi"]=cal_rsi(data)
    #data["perk"],data["perd"],data["slowd"]=cal_stk()
    #data["macd"],data["signal"]=cal_macd()
    #data["diup"],data["didown"],data["dx"],data["adx"]=cal_adx()
    #data2=data.copy()
    del data["time"]
    del data["Unnamed: 0"]
    data2=np.array(data)
    return data2

def predict_price(day,data):
    day_ago=day
    num_sihyou=data.shape[1]
    X=np.zeros((len(data),day_ago*num_sihyou))
    for s in range(0,num_sihyou):
        for i in range(0,day_ago):
            X[i:len(data),day_ago*s+i]=data[0:len(data)-i,s]
    print(X[-2,0])
    Y=np.zeros(len(data))
    pre_day=1
    Y[0:len(Y)-pre_day]=X[pre_day:len(X),0]-X[0:len(X)-pre_day,0]
    original_X=np.copy(X)
    tmp_mean=np.zeros((len(X),num_sihyou))
    for i in range(day_ago,len(X)):
        for s in range(num_sihyou):
            tmp_mean[i,s]=np.mean(original_X[i-day_ago+1:i+1,day_ago*s])
            for j in range(day_ago):
                X[i,day_ago*s+j]=(X[i,day_ago*s+j]-tmp_mean[i,s])
    n=int((len(X)-225)*0.8+225)
    X_train=X[225:n,:]
    Y_train=Y[225:n]
    X_test=X[n:len(X)-pre_day,:]
    Y_test=Y[n:len(Y)-pre_day]
    linear_reg_model=linear_model.LinearRegression()
    linear_reg_model.fit(X_train,Y_train)
    #print(linear_reg_model.intercept_)
    #print(linear_reg_model.coef_)
    Y_pred=linear_reg_model.predict(X_test)
    print(Y_pred[-1])
    if Y_pred[-1]<0:
        signal="SELL"
    else:signal="BUY"
    return signal

