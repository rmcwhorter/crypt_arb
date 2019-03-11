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

written_to_file = {}
unwritten = {}

current_time = time.time()

def streaming_func(asdf):
    #Ran until 1552289401728, which is 728 miliseconds longer than expected, which is perfect
    #time.time() < (current_time + (20*60))
    while(time.time() < (current_time + (60*40))):
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
                unwritten[df['Value']['ts']] = df
                print()
                print("Streaming:")
                print(df)
                print()
    
            else:
                pass



file = 'data/output_tmp.pkl'
def write_to_target(asdf):
    count = 0
    
    while (time.time() < (current_time + (60*40)+30)):
        time.sleep(15)
        #Get what we need to write to file
        local_unwritten = list(unwritten.keys())[:]
        
        d = dict((k, unwritten[k]) for k in local_unwritten if k in unwritten)
        
        with open(str('data/incremental_data/' + str(count) + '.pkl'), 'wb') as handle: pickle.dump(d, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
        written_to_file.update(d)
        for a in local_unwritten: unwritten.pop(a)
       
        print()
        print("Writing:")
        print('Wrote ',local_unwritten, ' to storage.')
        print()
        
        count += 1
        #print(local_unwritten)
        

thread1 = threading.Thread(target=write_to_target, args=(None,))
thread2 = threading.Thread(target=streaming_func, args=(None,))

# Will execute both in parallel
thread1.start()
thread2.start()

# Joins threads back to the parent process, which is this
    # program
thread1.join()
thread2.join()

print(written_to_file)
print(unwritten)

with open('data/master.pkl', 'wb') as handle: pickle.dump(written_to_file, handle, protocol=pickle.HIGHEST_PROTOCOL)

print("EOF")