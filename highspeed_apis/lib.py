'''
WebSockets APIs are generally faster than REST APIs because of the protocol redundency it drops
'''
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


ws = websocket.WebSocket()

base_url = 'wss://api.huobi.pro/hbus/ws'

def ping():
    ws = websocket.WebSocket()
    ws.connect(base_url)
    ws.send(json.dumps({'ping' : 18212558000}))
    result = ws.recv()
    decompressed_data = zlib.decompress(result, 16+zlib.MAX_WBITS)
    ws.close()
    print(decompressed_data)

def request(data):
    ws = websocket.WebSocket()
    ws.connect(base_url)
    ws.send(json.dumps(data))
    result = json.loads(zlib.decompress(ws.recv(), 16+zlib.MAX_WBITS).decode('utf8'))
    ws.close()
    return result


d = {
  "req": "market.ethusdt.kline.1min",
  "id": "id10",
  
}

#print(request(d)['data'])

ws = websocket.WebSocket()
ws.connect(base_url)
ws.send(json.dumps({
  "sub": "market.ethusdt.trade.detail",
  "id": "id1"
}))

dataframes = {}

def streaming_func(asdf):
    while (time.time() < (1552289400)):
        print()
        try:
            result = json.loads(zlib.decompress(ws.recv(), 16+zlib.MAX_WBITS).decode('utf8'))
        except:
            pass
        else:
            if('ping' in result.keys()):
                ws.send(json.dumps({'pong':time.time()}))
                #print(result)
            elif('ch' in result.keys()):
                #parse this into a pandas dataframe and print it
                df = pd.DataFrame.from_dict(result['tick']['data'][0],orient='index',columns=['Value'])
                dataframes[result['tick']['data'][0]['ts']] = df
                print(df)
    
            else:
                pass



file = 'data/data.pkl'
def write_to_target(asdf):
    while (time.time() < (1552289400 + 60)):
        if(time.time() % 30 == 0):
            with open(file, 'wb') as handle: pickle.dump(dataframes, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print("Wrote to file")

thread1 = threading.Thread(target=write_to_target, args=(None,))
thread2 = threading.Thread(target=streaming_func, args=(None,))

# Will execute both in parallel
thread1.start()
thread2.start()

# Joins threads back to the parent process, which is this
    # program
thread1.join()
thread2.join()

print("EOF")