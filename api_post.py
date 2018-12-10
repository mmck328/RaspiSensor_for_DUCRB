from dht11 import DHT11     
import tsl2561
import requests
import json
import time
import os

dht11 = DHT11()

SERVER = os.environ['UCITY_ABSTRACT_API_SERVER']
UCODE_TEMP = os.environ["UCODE_THERMOMETER"]
UCODE_HUMID = os.environ["UCODE_HYGROMETER"]
UCODE_ILLUMI = os.environ["UCODE_ILLUMINOMETER"]
INTERVAL = os.environ['SENSOR_INTERVAL']

HEADERS = {'Content-type': 'application/json'}

def postIlluminance():
    lux = tsl2561.getCalcLux()
    timestamp = time.strftime('%FT%T%z', time.localtime())
    
    try:
        url = SERVER + "/devices/" + UCODE_ILLUMI + "/state"
        body = {'value': lux, 'timestamp': timestamp}
        req = requests.put(url, data=json.dumps(body), headers=HEADERS, timeout=10.0)
        print(req.status_code)
    except:
        return False
    else:
        return True    

def postTemp():
    temperature = dht11.readTemp()
    timestamp = time.strftime('%FT%T%z', time.localtime())

    try:
        url = SERVER + "/devices/" + UCODE_TEMP + "/state"
        body = {'value': temperature, 'timestamp': timestamp}
        req = requests.put(url, data=json.dumps(body), headers=HEADERS, timeout=10.0)
        print(req.status_code)
    except:
        return False
    else:
        return True

def postHumidity():
    humidity = dht11.readHumidity()
    timestamp = time.strftime('%FT%T%z', time.localtime())
    
    try:
        url = SERVER + "/devices/" + UCODE_HUMID + "/state"
        body = {'value': humidity, 'timestamp': timestamp}
        req = requests.put(url, data=json.dumps(body), headers=HEADERS, timeout=10.0)
        print(req.status_code)
    except:
        return False
    else:
        return True

if __name__ == '__main__':
    try:
        while True:
            print("start")
            tStart = time.time()
            print("postIlluminance: ", end="")
            postIlluminance()
            print("postTemp: ", end="")
            postTemp()
            print("postHumidity: ", end="")
            postHumidity()
            print("end")
            tEnd = time.time()
            tWait = INTERVAL - (tEnd - tStart)
            time.sleep(max(0, tWait))
    except KeyboardInterrupt:
        pass
