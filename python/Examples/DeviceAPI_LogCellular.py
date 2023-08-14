#!/usr/bin/env python3
## Example of device API call script
## GPS logging to csv

import os
import requests
import json
import csv
import time

from dotenv import load_dotenv

load_dotenv()

server_prefix = os.getenv('server_prefix')
wan_id = os.getenv('wan_id')

if os.name == 'nt':
    HOME = os.getenv('appdata') + '\\PeplinkAPI'
    if not os.path.exists(HOME):
        os.makedirs(HOME)
else:
    HOME = os.getenv('HOME')

access_token_file = HOME + '/.access_token'
access_token = open(access_token_file, "r").read()

verify_ssl_cert = False

celllogfile = HOME + '/celllog.csv'

status_wan_connection_url = server_prefix + '/api/status.wan.connection'
info_location_url = server_prefix + '/api/info.location'

if not os.path.isfile(celllogfile):
    addcsvheader = True
else:
    addcsvheader = False

system_ts = 0
delaysec = 10

with open(celllogfile, 'a', encoding='UTF8', newline='') as CSVfile:
    CSVwriter = csv.writer(CSVfile)
    while True == True: #infinite loop
        if int(system_ts)+delaysec < int(time.time()):
            status_wan_connection_response = requests.get((status_wan_connection_url + "?accessToken=" + access_token), verify = verify_ssl_cert)
            info_location_response = requests.get((info_location_url + "?accessToken=" + access_token), verify = verify_ssl_cert)
            
            system_ts = time.time()
            datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            
            rqjson = json.loads(status_wan_connection_response.text)
            rqjsonloc = json.loads(info_location_response.text)

            Time = datetime

            if rqjsonloc["stat"] == 'ok':
                if rqjsonloc["response"]["gps"] == True:
                    Latitude = rqjsonloc["response"]["location"]["latitude"]
                    Longitude = rqjsonloc["response"]["location"]["longitude"]
                    Altitude = rqjsonloc["response"]["location"]["altitude"]
                else:
                    Latitude = ""
                    Longitude = ""
                    Altitude = ""
            else:
                print("Failed GPS data")
                print(info_location_response.text)

            if rqjson["stat"] == 'ok':
                loopn = 0
                bandslen = len(rqjson["response"][wan_id]["cellular"]["rat"][0]["band"])
                WAN_name = rqjson["response"][wan_id]["name"]
                Type = rqjson["response"][wan_id]["cellular"]["mobileType"]
                Cell_ID = rqjson["response"][wan_id]["cellular"]["cellTower"]["cellId"]
                Carrier = rqjson["response"][wan_id]["cellular"]["carrier"]["name"]
                Latency = -1 # api call for Latency?
                MNC = rqjson["response"][wan_id]["cellular"]["mnc"]
                MCC = rqjson["response"][wan_id]["cellular"]["mcc"]
                while bandslen > loopn:
                    Band = rqjson["response"][wan_id]["cellular"]["rat"][0]["band"][loopn]["name"]
                    LTE_RSRP = rqjson["response"][wan_id]["cellular"]["rat"][0]["band"][loopn]["signal"]["rsrp"]
                    LTE_SINR = rqjson["response"][wan_id]["cellular"]["rat"][0]["band"][loopn]["signal"]["sinr"]
                    LTE_RSRQ = rqjson["response"][wan_id]["cellular"]["rat"][0]["band"][loopn]["signal"]["rsrq"]
                    LTE_RSSI = rqjson["response"][wan_id]["cellular"]["rat"][0]["band"][loopn]["signal"]["rssi"]
                    CSV_DATA = {"WAN name": WAN_name, "Type": Type, "Cell ID": Cell_ID, "Carrier": Carrier, "Band": Band, "LTE - RSRP": LTE_RSRP, "LTE - SINR": LTE_SINR, "LTE - RSRQ": LTE_RSRQ, "LTE - RSSI": LTE_RSSI, "Latency": Latency, "MNC": MNC, "MCC": MCC, "Time": Time, "Latitude": Latitude, "Longitude": Longitude, "Altitude": Altitude}
                    if addcsvheader:
                        print("adding CSV headers")
                        CSVwriter.writerow(CSV_DATA.keys())
                        addcsvheader = False
                    print("adding CELL data")
                    CSVwriter.writerow(CSV_DATA.values())
                    CSVfile.flush()
                    loopn = loopn + 1
            else:
                print("Failed Cell data")
                print(status_wan_connection_response.text)
                exit(1)
