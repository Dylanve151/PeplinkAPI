#!/bin/bash

export $(cat .env)

admin_login='{"username":"'$admin_user'","password":"'$admin_pass'"}'

loginresponse=$(curl -k -c /tmp/cookies.txt -H "Content-Type: application/json" -X POST -d $admin_login ${server_prefix}/api/login)

clientresponse=$(curl -k -b /tmp/cookies.txt -H "Content-Type: application/json" -X POST -d '{"action":"add","name":"Client2","scope":"api"}' ${server_prefix}/api/auth.client)

echo $clientresponse
