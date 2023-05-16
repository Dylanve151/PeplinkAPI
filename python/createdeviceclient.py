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

if client_name == None:
    client_name = 'APIexample'

verify_ssl_cert = False

admin_login_url = server_prefix + '/api/login'
client_auth_url = server_prefix + '/api/auth.client'

admin_login_params = '?username=' + admin_user + '&password=' + admin_pass
loginresponse = requests.post((admin_login_url + admin_login_params), verify = verify_ssl_cert, headers = {'Content-type': 'application/x-www-form-urlencoded'})

client_auth_params = '?action=' + 'add' + '&name=' + client_name + '&scope=' + 'api'
clientresponse = requests.post((client_auth_url + client_auth_params), verify = verify_ssl_cert, headers = {'Content-type': 'application/x-www-form-urlencoded'}, cookies = loginresponse.cookies)

rqjson = json.loads(clientresponse.text)
if rqjson["stat"] == 'ok':
    print(rqjson["response"])
else:
    print(rqjson)