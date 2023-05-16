#!/bin/bash

export $(cat .env)

if [[ $client_name == "" ]] || [[ $client_name == $null ]]
then
    client_name='APIexample'
fi

admin_login_url=${server_prefix}'/api/login'
client_auth_url=${server_prefix}'/api/auth.client'

admin_login_params='{"username":"'$admin_user'","password":"'$admin_pass'"}'
loginresponse=$(curl -ks -c /tmp/cookies.txt -H "Content-Type: application/json" -X POST -d $admin_login_params $admin_login_url)

client_auth_params='{"action":"add","name":"'$client_name'","scope":"api"}'
clientresponse=$(curl -ks -b /tmp/cookies.txt -H "Content-Type: application/json" -X POST -d $client_auth_params $client_auth_url)

if [[ $(echo $clientresponse | jq -r .stat) == "ok" ]]
then
    echo $clientresponse | jq -r .response
else
    echo $clientresponse | jq -r .
fi
