#!/bin/bash
## Example of device API call script
## Send sms

export $(cat .env)

# please change these variables
smsnumber="1234567890"
smsmessage="Some text"
connid="2"
simid="1"

## Token file
access_token_file="${HOME}/.access_token"
access_token=$(cat ${access_token_file})

tmpfile="/tmp/ic2.tmpfile.$$"

curl_opt=" -k "

token_params="accessToken=${access_token}"
sendsms_params="&connId=${connid}&address=${smsnumber}&content=${smsmessage}"

curl $curl_opt -so $tmpfile --data "${token_params}${sendsms_params}" "${api_server_prefix}/api/cmd.sms.sendMessage"

stat=$(jq -r ".stat" $tmpfile)
if [ "${stat}" == "ok" ]
then
  echo "OK: SMS has been send"
else
  echo "FAIL: SMS has NOT been send"	
fi

rm -f $tmpfile
