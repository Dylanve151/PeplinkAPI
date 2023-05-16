#!/bin/bash

export $(cat .env)

if [[ $client_name == "" ]] || [[ $client_name == $null ]]
then
    client_name='APIexample'
fi

remove_id="samename" #all, samename, choose

admin_login_url=${server_prefix}'/api/login'
client_auth_url=${server_prefix}'/api/auth.client'

admin_login_params='{"username":"'$admin_user'","password":"'$admin_pass'"}'
loginresponse=$(curl -ks -c /tmp/cookies.txt -H "Content-Type: application/json" -X POST -d $admin_login_params $admin_login_url)

clientgetresponse=$(curl -ks -b /tmp/cookies.txt -H "Content-Type: application/json" -X GET $client_auth_url)

if [ $remove_id == "all" ]
then
    rclient_ids=$(echo $clientgetresponse | jq -r '.response[].clientId')
elif [ $remove_id == "samename" ]
then
    rclient_ids=($(echo $clientgetresponse | jq -r '.response[] | select(.name=="'${client_name}'") | .clientId'))
    rclient_ids=${rclient_ids[@]/$client_id}
elif [ $remove_id == "choose" ]
then
    rclient_ids=($(echo $clientgetresponse | jq -r '.response[].clientId'))
    idn=0
    for rclient_id in "${rclient_ids[@]}"
    do
        echo "$idn: $rclient_id"
        ((idn+=1))
    done
    read -p "Number: " chooseid
    rclient_ids=${rclient_ids[$chooseid]}
fi

for rclient_id in $rclient_ids
do
    rclient_auth_params='{"action":"remove","clientId":"'$rclient_id'"}'
    rclientresponse=$(curl -ks -b /tmp/cookies.txt -H "Content-Type: application/json" -X POST -d $rclient_auth_params $client_auth_url)
    if [[ $(echo $rclientresponse | jq -r .stat) == "ok" ]]
    then
        echo 'Removed: '$rclient_id
    else
        echo 'Failed: '$rclient_id
    fi
done