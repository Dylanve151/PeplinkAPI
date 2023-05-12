#!/usr/bin/env python3

import os
import requests

from dotenv import load_dotenv

load_dotenv()

admin_user = os.getenv('admin_user')
admin_pass = os.getenv('admin_pass')
server_prefix = os.getenv('server_prefix')

verify_ssl_cert = False

admin_login_url = server_prefix + '/api/login'
client_create_url = server_prefix + '/api/auth.client'

admin_login_params = '?username=' + admin_user + '&password=' + admin_pass
loginresponse = requests.post((admin_login_url + admin_login_params), verify = verify_ssl_cert, headers = {'Content-type': 'application/x-www-form-urlencoded'})

client_create_params = '?action=' + 'add' + '&name=' + 'Client2' + '&scope=' + 'api'
tmpresponse = requests.post((client_create_url + client_create_params), verify = verify_ssl_cert, headers = {'Content-type': 'application/x-www-form-urlencoded'}, cookies = loginresponse.cookies)

print(tmpresponse.text)