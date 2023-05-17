#!/usr/bin/env python3

import os
import requests
import json

from dotenv import load_dotenv

load_dotenv()

admin_user = os.getenv('admin_user')
admin_pass = os.getenv('admin_pass')
server_prefix = os.getenv('server_prefix')
client_name = os.getenv('client_name')
client_id = os.getenv('client_id')

if client_name == None:
    client_name = 'APIexample'

verify_ssl_cert = False

remove_id = "samename" #all, samename, choose

admin_login_url = server_prefix + '/api/login'
client_auth_url = server_prefix + '/api/auth.client'

admin_login_params = '?username=' + admin_user + '&password=' + admin_pass
loginresponse = requests.post((admin_login_url + admin_login_params), verify = verify_ssl_cert, headers = {'Content-type': 'application/x-www-form-urlencoded'})

clientgetresponse = requests.get((client_auth_url), verify = verify_ssl_cert, headers = {'Content-type': 'application/x-www-form-urlencoded'}, cookies = loginresponse.cookies)

rqjson = json.loads(clientgetresponse.text)
rclient_ids = []

if remove_id == "all":
    for x in rqjson["response"]:
        rclient_ids.append(x["clientId"])
elif remove_id == "samename":
    for x in rqjson["response"]:
        if x["name"] == client_name:
            rclient_ids.append(x["clientId"])
    if client_id in rclient_ids:
        rclient_ids.remove(client_id)
elif remove_id == "choose":
    idn = 0
    for x in rqjson["response"]:
        rclient_ids.append(x["clientId"])
        print(str(idn) + ": " + x["clientId"])
        idn += 1
    chooseid = input("Number: ")
    rclient_ids=[rclient_ids[int(chooseid)]]


for rclient_id in rclient_ids:
    client_auth_params = '?action=' + 'remove' + '&clientId=' + rclient_id
    clientresponse = requests.post((client_auth_url + client_auth_params), verify = verify_ssl_cert, headers = {'Content-type': 'application/x-www-form-urlencoded'}, cookies = loginresponse.cookies)
    rqjson2 = json.loads(clientresponse.text)
    if rqjson2["stat"] == 'ok':
        print("Removed: " + rclient_id)
    else:
        print("Failed: " + rclient_id)

