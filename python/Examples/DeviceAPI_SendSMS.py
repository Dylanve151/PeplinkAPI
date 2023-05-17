#!/usr/bin/env python3

import os
import requests
import json

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

# please change these variables
send_sms_connId = 3
send_sms_address = "0123456789"
send_sms_content = "Hello"

verify_ssl_cert = False

send_sms_url = server_prefix + '/api/cmd.sms.sendMessage'
test_url = server_prefix + '/api/cmd.wan.cellular'

send_sms_params = {"connId": send_sms_connId, "address": send_sms_address, "content": send_sms_content}
send_sms_response = requests.post((send_sms_url + "?accessToken=" + access_token), verify = verify_ssl_cert, headers = {'Content-type': 'application/json'}, json=send_sms_params)

print(send_sms_response.text)
