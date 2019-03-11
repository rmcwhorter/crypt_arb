'''
We need ETH-USD quotes for these various exchanges.
We also need some metric of volume, probably 24hr volume, or like 15 minute volume
We will also invariably want to compute volatility for each exchange.

Okex - doesn't serve customers in a number of countries, including the USA. Assholes.
Bit-Z:
        API Key： d1e6d1316b76117d9f3d05d03cedc70e
        Secret： FbJt7lnEJEi2V9irnryuVQ0OlKc4fI1f4s2bT7vWr2ZNJp8nu2M5FNk5QdS4ZNN6
        mean query time for 100 requests on utexas wifi is 0.3481269335746765 seconds
HitBTC:
    Don't think this supports US based traders, created a Canadian account anyways
Bitnance:
    If domain is bitnance.vip, then this is a chinese website with no english translation
BitFinex:
    Requires a minimum equity of 10K USD
    Can't actually get API keys until you meet this requirement    
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
Bithumb
Coinbase
Kraken
Bitstamp
CEX.IO
Gemini
Quoine
Liquid
bitFlyer
BitMEX
Poloniex
BitSquare
Bittrex
QuadrigaCX
Luno
BitBay
CoinOne
CryptoFacilities
'''
import requests
import time
import numpy as np
import pandas as pd
from interruptingcow import timeout
import threading

def bitz_request(symbol, standardized = True):
    #symbol should be of the format 'eth_usdt'
    #Returns a pandas dataframe with all the useful information
    base_urls = ['https://apiv2.bitz.com','https://apiv2.bit-z.pro','https://api.bitzapi.com','https://api.bitzoverseas.com','https://api.bitzspeed.com']
    url_extension = "/Market/ticker"
    params = {'symbol' : symbol}
    
    s = None
    u_index = 0
    u_max_index = 5
    
    while(s == None):
        url = base_urls[int(u_index % u_max_index)] + url_extension
        try:
            with timeout(0.5, exception=RuntimeError):
                s = requests.get(url = url, params = params).json()['data']
        except(RuntimeError): 
            print("Timed out operation")
            u_index += 1
    
    df = pd.DataFrame.from_dict(s, orient='index', columns=['Values'])
    
    #Note, the standardized function lets us drop all unnecessary data this specific exchange might send us.
    if(standardized):
        #The canonical list of data we want to recieve is ask, bid, last, open, high, low, close, volume
        df.drop(index=['jpy','krw','cny','pricePrecision','numberPrecision','lastId','firstId','symbol','priceChange','priceChange24h','askQty','bidQty','dealCount','usd','quoteVolume'], inplace=True)
        df.rename({'askPrice':'ask','bidPrice':'bid','now':'last'}, inplace=True)
        df.sort_index(inplace=True)
    df = df.astype('float')
        
        
    
    return df

def hitbtc_request(symbol, standardize = True):
    #symbol shouldbe of the format 'ETHUSD'
    #Ex symbol = "ETHUSD"
    url = 'https://api.hitbtc.com/api/2/public/ticker/' + symbol
    
    s = requests.get(url=url).json()
    df = pd.DataFrame.from_dict(s, orient='index', columns=['Values'])
    
    if(standardize):
        #The canonical list of data we want to recieve is ask, bid, last, open, high, low, close, volume
        df.drop(index=['timestamp','symbol','volumeQuote'], inplace=True)
        df.sort_index(inplace=True)
    df = df.astype('float')
    
    return df






