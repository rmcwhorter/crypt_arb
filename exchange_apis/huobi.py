#!/usr/bin/python
'''
Huobi:
    Access Key: 04d2c7da-26786a3c-0af87097-48d99
    Private Key: cbd44709-fed7ac60-53ba35ad-f30a1
    NOTE: This key expires in 90 days, since it isn't bound to an IP Address
    
    The REST API:
        URL for market data: https://api.huobi.com/market #You can access this without API kets, because it is public
        URL for executing trades: https://api.huobi.com/v1 #requires API keys
        Requires HTTPS
        Max of 10 HTTPS requests per second
        
        Format of a response to a request:
            //success
            {
            	"status": "ok",
            	"data":  Response data
            }
            
            //error
            {
            	"status": "error",
            	"data":  null,
            	"err-code": "login-required",
            	"err-msg": "Please login first"
            }
        
        Example symbol: btcusdt -> Bitcoin quote in USDT
        
        
    Huobi also offers a Websocket API, but what the fuck is that?
'''
import requests
import time
import numpy as np
import pandas as pd
from interruptingcow import timeout
import threading

#The canonical list of data we want to recieve for a market request is ask, bid, last, open, high, low, close, volume

#GET /market/detail/merged Get Ticker
def huobi_request(symbol, standardize=True):
    url = 'https://api.huobi.com/market/detail/merged'
    params = {'symbol':symbol}
    data = requests.get(url=url, params = params).json()
    
    if(data['status'] == 'ok'):
        df = pd.DataFrame.from_dict(data['tick'], orient='index', columns=['Values'])
        if(standardize):
            df.drop(index=['amount','id','count','version'], inplace=True)
            df.rename({'vol':'volume','close':'last'}, inplace=True)
            
            df['Values']['ask'] = df['Values']['ask'][0]
            df['Values']['bid'] = df['Values']['bid'][0]
            
            df.sort_index(inplace=True)
        return df
    elif(data['status'] == 'error'):
        print(data['err-msg'])
    else:
        print("Error occured, likely timed out")
