print("SOF")

import requests
import time
import numpy as np
import pandas as pd
from interruptingcow import timeout
import threading
import request_lib as rl


bitz_account = []
hitbtc_account = []

start_time = time.time()

z = 100
t = 0.7
for _ in range(z):
    bitz = rl.bitz_request("eth_usdt")
    hitbtc = rl.hitbtc_request("ETHUSD")
        
    if(bitz.loc['ask']['Values'] > hitbtc.loc['bid']['Values']):
        bitz_account.append(float(bitz.loc['ask']['Values']))
        hitbtc_account.append(-1 * float(hitbtc.loc['bid']['Values']))
        
        print("HitBTC -> BitZ: ", "buy = ", float(bitz.loc['ask']['Values']), " sell = ", -1 * float(hitbtc.loc['bid']['Values']), " spread = ", float(bitz.loc['ask']['Values']) + -1 * float(hitbtc.loc['bid']['Values']))
    else:
        hitbtc_account.append(float(hitbtc.loc['bid']['Values']))
        bitz_account.append(-1 * float(bitz.loc['ask']['Values']))
        
        print("BitZ -> HitBTC: ", "buy = ", -1 * float(bitz.loc['ask']['Values']), " sell = ", float(hitbtc.loc['bid']['Values']), " spread = ", -1 * float(bitz.loc['ask']['Values']) + float(hitbtc.loc['bid']['Values']))
    print("Net Profit = ", np.sum(bitz_account) + np.sum(hitbtc_account))
    print()
        
    
    time.sleep(t)

end_time = time.time()

print(np.sum(bitz_account) + np.sum(hitbtc_account)/(end_time - start_time - (z*t)), " dollars/second")

print("EOF")