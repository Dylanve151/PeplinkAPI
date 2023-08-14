#!/bin/bash
## Example of device API call script
## Cell logging to csv

export $(cat .env)

# please change these variables
templogfile="${HOME}/celllog.csv"

## Token file
access_token_file="${HOME}/.access_token"
access_token=$(cat ${access_token_file})

tmpfile="/tmp/ic2.tmpfile.$$"
tmpfile2="/tmp/ic2.tmpfile2.$$"

touch $tmpfile
touch $tmpfile2

curl_opt=" -k "

echo "Logging Cell data..."

token_params="accessToken=${access_token}"
echo $token_params
curl $curl_opt -so $tmpfile --data "${token_params}" "${server_prefix}/api/info.location"
curl $curl_opt -so $tmpfile2 "${server_prefix}/api/status.wan.connection?${token_params}"
reqstatgps=$(jq -r '.stat' $tmpfile)
if grep -q Unauthorized $tmpfile ; then
	echo "The saved access token is invalid."
	jq -r '.' $tmpfile
	rm -f ${access_token_file}
	exit 7
fi

if [ "${reqstatgps}" == "fail" ] ; then
	echo "Failed GPS data"
	jq -r '.' $tmpfile
	exit 7
fi

if [ -f "$templogfile" ]; then
		echo "GPS logged"
else
		csvhead="WAN name;Type;Cell ID;Carrier;Band;LTE - RSRP;LTE - SINR;LTE - RSRQ;LTE - RSSI;Latency;MNC;MCC;Time;Latitude;Longitude;Altitude"
		echo ${csvhead} > $templogfile
		echo "File created with csv head"
fi

ts=$(date +"%s")
datetime=$(date +"%Y-%m-%d %H:%M:%S")

gpsstat=$(jq -r '.response.gps' $tmpfile)
if [ "${gpsstat}" == "true" ] ; then
	latitude=$(jq -r '.response.location.latitude' $tmpfile)
	longitude=$(jq -r '.response.location.longitude' $tmpfile)
	altitude=$(jq -r '.response.location.altitude' $tmpfile)
else
	latitude=""
	longitude=""
	altitude=""
fi

cellstat=$(jq -r '.stat' $tmpfile2)
if [ "${cellstat}" == "ok" ] ; then
	loopn=0
	bandslen=$(jq -r ".response.\"${wan_id}\".cellular.rat[0].band | length" $tmpfile2)
	WAN_name=$(jq -r ".response.\"${wan_id}\".name" $tmpfile2)
	Type=$(jq -r ".response.\"${wan_id}\".cellular.mobileType" $tmpfile2)
	Cell_ID=$(jq -r ".response.\"${wan_id}\".cellular.cellTower.cellId" $tmpfile2)
	Carrier=$(jq -r ".response.\"${wan_id}\".cellular.carrier.name" $tmpfile2)
	Latency=-1
	MNC=$(jq -r ".response.\"${wan_id}\".cellular.mnc" $tmpfile2)
	MCC=$(jq -r ".response.\"${wan_id}\".cellular.mcc" $tmpfile2)
	while [ $bandslen -gt $loopn ]
	do
		band=$(jq -r ".response.\"${wan_id}\".cellular.rat[0].band[${loopn}].name" $tmpfile2)
		LTE_RSRP=$(jq -r ".response.\"${wan_id}\".cellular.rat[0].band[${loopn}].signal.rsrp" $tmpfile2)
		LTE_SINR=$(jq -r ".response.\"${wan_id}\".cellular.rat[0].band[${loopn}].signal.sinr" $tmpfile2)
		LTE_RSRQ=$(jq -r ".response.\"${wan_id}\".cellular.rat[0].band[${loopn}].signal.rsrq" $tmpfile2)
		LTE_RSSI=$(jq -r ".response.\"${wan_id}\".cellular.rat[0].band[${loopn}].signal.rssi" $tmpfile2)
		csvdata="${WAN_name};${Type};${Cell_ID};${Carrier};${band};${LTE_RSRP};${LTE_SINR};${LTE_RSRQ};${LTE_RSSI};${Latency};${MNC};${MCC};${datetime};${latitude};${longitude};${altitude}"
		echo ${csvdata} >> $templogfile
		loopn=$(($loopn + 1))
	done
else
	echo "Failed Cell data"
	jq -r '.' $tmpfile2
	exit 7
	
fi

rm -f $tmpfile
rm -f $tmpfile2
