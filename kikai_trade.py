import hashlib
import hmac
import requests
from datetime import datetime
import json
import ccxt
from pprint import pprint
import time
import numpy as np
import pandas as pd
import os
from os.path import join, dirname
from dotenv import load_dotenv
from kikai3 import dataset,predict_price
"""
ccxtの設定、apiキー入力
"""
load_dotenv(join(dirname(__file__),".env"))

key=os.environ.get("API_KEY")
secret=os.environ.get("API_SECRET")

bitflyer = ccxt.bitflyer()
bitflyer.apiKey = key
bitflyer.secret = secret



def buy ():
    """
    成行買
    """
    try:
       bitflyer.create_order(
            symbol = "BTC/JPY",
            type = "market",
            side = "buy",
            amount = '0.01',
            params = {"product_code" :"FX_BTC_JPY"})

    except ccxt.BaseError as e:
        print("BitflyerのAPIでエラー1発生： ", e)
def sell ():
    """
    成行売
    """
    try:
        bitflyer.create_order(
                symbol = "BTC/JPY",
                type = "market",
                side = "sell",
                amount = '0.01',
                params = {"product_code" :"FX_BTC_JPY"})
    except ccxt.BaseError as e:
        print("BitflyerのAPIでエラー2発生： ", e)

def check_position():
    """
    現在のポジションを確認する関数
    """
    try:
        position = bitflyer.private_get_getpositions(params = { "product_code" : "FX_BTC_JPY"})
        side = position[0]['side']
        return side
    except ccxt.BaseEroor as e:
        print("BitflyerのAPIで問題発生： ",e)
        time.sleep(10)


#buy()

side=check_position()
print(side)
data=dataset()
signal=predict_price(35,data)
print(signal)
if side=="SELL" and signal=="BUY":
    buy()
    buy()
    print("BUY")
elif side=="BUY" and signal == "SELL":
    sell()
    sell()
    print("SELL")
else:
    print("hold")
