#!/usr/bin/python
print("SOF")

import requests
import time
import numpy as np
import pandas as pd
from interruptingcow import timeout
import threading
import request_lib as rl

from exchange_apis import huobi






z = 50
t = 0.7

#We want to find the cheapest value on each exchange, buy it, then sell it on the most expensive exchange

bitz_symbol = 'eth_usdt'
hitbtc_symbol = 'ETHUSD'
huobi_symbol = 'ethusdt'

bitz_account = []
hitbtc_account = []
huobi_account = []

accounts_dict = {'bitz':bitz_account,
                 'hitbtc':hitbtc_account,
                 'huobi':huobi_account}

start_time = time.time()
position = 0
for _ in range(z):
    exchange_requests = {'bitz':rl.bitz_request(bitz_symbol),
                'hitbtc':rl.hitbtc_request(hitbtc_symbol),
                'huobi':huobi.huobi_request(huobi_symbol)}
    
    current_prices = {}
    for a in exchange_requests:
        current_prices[a] = exchange_requests[a]['Values']['last']
        
    max_price = max(current_prices, key=current_prices.get)
    min_price = min(current_prices, key=current_prices.get)
    
    print()
    print("Buying from " + min_price + " at " + str(current_prices[min_price]) + " and selling to " + max_price + " at " + str(current_prices[max_price]) + " for a spread of " + str(current_prices[max_price] - current_prices[min_price]))
    accounts_dict[max_price].append(current_prices[max_price])
    accounts_dict[min_price].append(-1 * current_prices[min_price])
    
    position += current_prices[max_price] - current_prices[min_price]
    print("Current profits are ", str(position))
    
    time.sleep(t)
    
end_time = time.time()

print("Averaged " + str(position / (end_time - start_time - (z*t))) + " dollars per second")   