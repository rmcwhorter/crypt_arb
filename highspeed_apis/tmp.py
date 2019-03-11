print("SOF")
import time as t
import numpy as np
import pandas as pd
from interruptingcow import timeout as to
import threading
import websocket
import json
import zlib
import time
import pickle
from os import listdir
from os.path import isfile, join
import matplotlib as mpl

with open('data/master_pandas.pkl', 'rb') as handle: master_df = pickle.load(handle)

'''
                             Value
amount                        4.58
ts                   1552334315513
id         10063794288226494086305
price                       131.58
direction                     sell
'''

timestamp = master_df.index.values
price = []
amount = []
direction = []
price_percent = []

for a in master_df['order']:
    price.append(a['Value']['price'])
    amount.append(a['Value']['amount'])
    
    d = a['Value']['direction']
    if(d == 'buy'):
        direction.append(1)
    else:
        direction.append(-1)
    
for a in range(len(price)):
    price_percent.append((price[a]/price[a-1]) - 1)
        
price = np.array(price)
amount = np.array(amount)
direction = np.array(direction)
price_percent = np.array(price_percent)

range_plot = np.array(range(timestamp[-1] - timestamp[0]))

adjusted_prices = []
adjusted_amount = []
adjusted_direction = []
adjusted_pad = []
adjusted_price_percent = []

price_stats = {'price_mean' : np.mean(price),
'price_median' : np.median(price),
'price_stdev' : np.std(price)}

amount_stats = {'amount_mean' : np.mean(amount),
                'amount_median' : np.median(amount),
                'amount_stdev' : np.std(amount)}

direction_stats = {'direction_mean' : np.mean(direction),
                   'direction_median' : np.median(direction),
                   'direction_stdev' : np.std(direction)}

price_amount_direction = price*amount*direction

pad_stats = {'pad_mean' : np.mean(price_amount_direction),
             'pad_median' : np.median(price_amount_direction),
             'pad_stdev' : np.std(price_amount_direction)}

print(price_stats)
print()
print(amount_stats)
print()
print(direction_stats)
print()
print(pad_stats)
print()

count = 0
count_2 = 0

for a in range_plot:
    if(a + timestamp[0] in timestamp):
        adjusted_prices.append(master_df['order'][a + timestamp[0]]['Value']['price'])
        adjusted_amount.append(master_df['order'][a + timestamp[0]]['Value']['amount'])
        
        d = master_df['order'][a + timestamp[0]]['Value']['direction']
        if(d == 'buy'):
            adjusted_direction.append(1)
        else:
            adjusted_direction.append(-1)
        
        adjusted_pad.append(price_amount_direction[count])
        count += 1
        adjusted_price_percent.append(price_percent[count_2])
        
    else:
        adjusted_prices.append(adjusted_prices[-1])
        adjusted_amount.append(0)
        adjusted_direction.append(0)
        adjusted_pad.append(0)
        adjusted_price_percent.append(0)
        
adjusted_prices = np.array(adjusted_prices)
adjusted_amount = np.array(adjusted_amount)
adjusted_direction = np.array(adjusted_direction)
adjusted_pad = np.array(adjusted_pad)
adjusted_price_percent = np.array(adjusted_price_percent)


mpl.pyplot.figure(0)
mpl.pyplot.plot(range_plot,adjusted_prices)
mpl.pyplot.figure(1)
mpl.pyplot.plot(range_plot,adjusted_amount)
mpl.pyplot.figure(2)
mpl.pyplot.plot(range_plot,adjusted_direction)
mpl.pyplot.figure(3)
mpl.pyplot.plot(range_plot,adjusted_pad)
mpl.pyplot.figure(3)
mpl.pyplot.plot(timestamp, price_percent)
mpl.pyplot.plot(timestamp, direction)



print(np.corrcoef([adjusted_prices,adjusted_amount,adjusted_direction,adjusted_pad,adjusted_price_percent]))
print()
print(np.corrcoef([price, amount, direction, price_amount_direction, price_percent]))




print("EOF")