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

if os.name == 'nt':
    HOME = os.getenv('appdata') + '\\PeplinkAPI'
    if not os.path.exists(HOME):
        os.makedirs(HOME)
else:
    HOME = os.getenv('HOME')

access_token_file = HOME + '/.access_token'
access_token = open(access_token_file, "r").read()

verify_ssl_cert = False

gpslogfile = HOME + '/gpslog.csv'

info_location_url = server_prefix + '/api/info.location'

if not os.path.isfile(gpslogfile):
    addcsvheader = True
else:
    addcsvheader = False

system_ts = 0

with open(gpslogfile, 'a', encoding='UTF8', newline='') as CSVfile:
    CSVwriter = csv.writer(CSVfile)
    while True == True: #infinite loop
        if system_ts < int(time.time()):
            info_location_response = requests.get((info_location_url + "?accessToken=" + access_token), verify = verify_ssl_cert)
            system_ts = int(time.time())

            rqjson = json.loads(info_location_response.text)
            if rqjson["stat"] == 'ok':
                if rqjson["response"]["gps"] == True:
                    gps_ts = rqjson["response"]["location"]["timestamp"]
                    gps_la = rqjson["response"]["location"]["latitude"]
                    gps_lo = rqjson["response"]["location"]["longitude"]
                    gps_at = rqjson["response"]["location"]["altitude"]
                    CSV_DATA = {"ts": system_ts, "gps_ts": gps_ts, "la": gps_la, "lo": gps_lo, "at": gps_at}
                    if addcsvheader:
                        print("adding CSV headers")
                        CSVwriter.writerow(CSV_DATA.keys())
                        addcsvheader = False
                    print("adding GPS data")
                    CSVwriter.writerow(CSV_DATA.values())
                    CSVfile.flush()
                else:
                    print("No GPS")
            else:
                print("Failed")
                print(info_location_response.text)
                exit(1)


