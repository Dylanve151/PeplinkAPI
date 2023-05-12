#!/usr/bin/env python3

import os
import requests
import json
import random
import time

from dotenv import load_dotenv

load_dotenv()

server_type = os.getenv('server_type')
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
server_prefix = os.getenv('server_prefix')
grant_type = os.getenv('grant_type')
redirect_uri = os.getenv('redirect_uri')
if os.name == 'nt':
    HOME = os.getenv('appdata') + '\\PeplinkAPI'
    if not os.path.exists(HOME):
        os.makedirs(HOME)
else:
    HOME = os.getenv('HOME')

# For InControl 2, the server_prefix is https://api.ic.peplink.com.
# For InControl appliances, this is https://{SERVER_NAME_HERE}.
if server_prefix == None:
    if server_type == "device":
        server_prefix = "http://192.168.50.1"
    else:
        server_prefix = "https://api.ic.peplink.com"


if redirect_uri == None:
    redirect_uri = "http://peplink.com"


# For InControl 2, set 1 to verify the API service's SSL certificate.
# For InControl appliances without a valid SSL certificate, set this to 0 to ignore the certificate validity.
if server_type == "device":
    verify_ssl_cert = False
else:
    verify_ssl_cert = True

################# Code for OAuth2 token handling goes below ##################
access_token_file = HOME + '/.access_token'
refresh_token_file = HOME + '/.refresh_token'
tmpfile = '/tmp/ic2.tmpfile.' + str(random.randint(0, 999))
if server_type == "device":
    grant_token_url = server_prefix + '/api/auth.token.grant'
else:
    #incontrol2 token endpoint
    grant_token_url = server_prefix + '/api/oauth2/token'
    #incontrol2 authorization endpoint
    ic2_auth_url = server_prefix + '/api/oauth2/auth?client_id=' + client_id + '&response_type=code'

    if client_id == None or client_secret == None:
        print("Please enter Client ID and Client Secret")
        exit(1)
    
    if grant_type == "authorization_code" and redirect_uri == None:
        print("Please enter redirect uri")
        exit(1)

if server_type == "device":
    def save_tokens(*args):
        rqjson = json.loads(args[0])
        if rqjson["stat"] == 'ok':
            rjson = rqjson["response"]
            access_token_tmp = rjson["accessToken"]
            expires_in = rjson["expiresIn"]
        else:
            print("Unable to obtain an access token. Process aborted")
            print("Returned" + rqjson)
            exit(3)
        f = open(access_token_file, "w")
        f.write(access_token_tmp)
        f.close()
        os.utime(access_token_file, ((time.time() + expires_in), (time.time() + expires_in)))
else:
    def save_tokens(*args):
        rqjson = json.loads(args[0])
        if rqjson["stat"] == 'ok':
            rjson = rqjson
            access_token_tmp = rjson["access_token"]
            refresh_token_tmp = rjson["refresh_token"]
            expires_in = rjson["expiresIn"]
        else:
            print("Unable to obtain an access token. Process aborted")
            print("Returned" + rqjson)
            exit(3)
        f = open(access_token_file, "w")
        f.write(access_token_tmp)
        f.close()
        f = open(refresh_token_file, "w")
        f.write(refresh_token_tmp)
        f.close()
        os.utime(access_token_file, ((time.time() + expires_in), (time.time() + expires_in)))
        os.utime(refresh_token_file, ((time.time() + expires_in + (30*60*60)), (time.time() + expires_in + (30*60*60))))

if os.path.isfile(access_token_file):
    if os.path.getctime(access_token_file) > (time.time() + (6*60)):
        access_token = open(access_token_file, "r").read()
    elif os.path.isfile(refresh_token_file):
        if os.path.getctime(refresh_token_file) > (time.time() + (6*60)):
            refresh_token = open(refresh_token_file, "r").read()
            #grant_token_params = 'client_id=' + client_id + '&client_secret=' + client_secret + '&grant_type=refresh_token&refresh_token=' + refresh_token
            grant_token_json = {'client_id': client_id, 'client_secret': client_secret, 'grant_type': 'refresh_token', 'refresh_token': refresh_token}
            tmpresponse = requests.post(grant_token_url, json = grant_token_json, verify = verify_ssl_cert)
            save_tokens(tmpresponse.text)
        else:
            os.remove(access_token_file)
            os.remove(refresh_token_file)

if not os.path.isfile(access_token_file):
    if grant_type == "authorization_code" and server_type != "device":
        print("")
        print("Start a web browser, visit the following URL and follow the instructions.")
        print("")
        print(ic2_auth_url)
        print("")
        print("You will be redirected to" + redirect_uri + "?code=CODE_HERE")
        code = input('Please enter the \'code\' in the redirected URL here:\n')

        if code == None:
            print("Error: The code is empty.  Process aborted")
            exit(5)

        grant_token_json = {'client_id': client_id, 'client_secret': client_secret, 'grant_type': 'authorization_code', 'code': code, 'redirect_uri': redirect_uri}
    else:
        if server_type == "device":
            grant_token_json = {'clientId': client_id, 'clientSecret': client_secret, 'scope': 'api'}
        else:
            grant_token_json = {'client_id': client_id, 'client_secret': client_secret, 'grant_type': 'client_credentials'}
    
    tmpresponse = requests.post(grant_token_url, json = grant_token_json, verify = verify_ssl_cert)
    save_tokens(tmpresponse.text)
