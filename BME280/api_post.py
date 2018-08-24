#coding: utf-8

import bme280
import tsl2561
import requests
import json
import time
import csv
import ipget

SERVER = ""
DEV_UCODE = ""
HEADERS = {'Content-type': 'application/json'}

def getRaspiInfo():
    url = SERVER + "/api/" + DEV_UCODE + "/raspiinfo/"
    r = requests.get(url=url)
    return r.json()

def postRaspiIpaddress():
    url = SERVER + "/api/raspiipaddress/"
    ip = ipget.ipget()
    ipaddress = ip.ipaddr("wlan0")

    data = {
        "dev_ucode": DEV_UCODE,
        "ip": ipaddress
    }

    try:
        conn = requests.post(url=url, data=json.dumps(data), headers=HEADERS, timeout=30.0)
    except:
        time.sleep(10)
        postRaspiIpaddress()

def postData(infoList):
    temperature, pressure, humidity = bme280.getBME280All()
    dataList = [temperature, humidity, pressure]
    
    """
    print("temp = %f" % temperature)
    print("humi = %f" % humidity)
    print("pres = %f" % pressure)
    """

    url = SERVER + "/api/koshizuka-lab/raspisensorstate/"
        
    count = 0
    for data in infoList:
        data["value"] = dataList[count]
        
        try:
            conn = requests.post(url=url, data=json.dumps(data), headers=HEADERS, timeout=30.0)
            #print(conn.status_code)
            count+=1
        except TimeoutError:
            #print("TimeoutError")
            return False
        except requests.exceptions.ConnectionError:
            #print("Connection_Error")
            return False
    return True
        
if __name__ == '__main__':
    try:
        infoList = getRaspiInfo()
        postRaspiIpaddress()
        while True:
            if postData(infoList):
                time.sleep(60)
            else:
                continue
    except KeyboardInterrupt:
        pass

