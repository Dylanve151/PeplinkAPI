# PeplinkAPI-Examples

## Running locally Bash on debian

### Install requirements
```bash
sudo apt-get update
sudo apt-get install -y curl jq
```

```bash
./bash/apitoken.bash
```

## Running locally Python

### Install requirements
```bash
pip install -r ./python/requirements.txt
```

```bash
python ./python/apitoken.py
```

## variables for .env file
Copy `.env.example` to `.env` and replace variables in the file

### Required IC2 API:
* client_id=
* client_secret=
* grant_type=**client_credentials** or **authorization_code** (Default: **client_credentials** (requires no interaction))

### Optional IC2 API:
* redirect_uri=For example: https://peplink.com (Only required when using **authorization_code** (requires interaction))
* server_type=**device** or **ic2** (Default: **ic2** when using incontrol2 api. **device** when using device api.)
* server_prefix=By default https://api.ic.peplink.com for use with https://incontrol2.peplink.com

### Required Device API:
* client_id=
* client_secret=
* server_prefix=Use IP address or hostname of device with http:// or https:// leading (By default https://api.ic.peplink.com for use with https://incontrol2.peplink.com)
* server_type=**device** (Default: **ic2** when using incontrol2 api. **device** when using device api.)

### Optional Device API:
* admin_user=Admin username for webgui login. (Only needed for creating client ID + client secret.)
* admin_pass=Admin password for webhui login. (Only needed for creating client ID + client secret.)
* server_type=**device** or **ic2** (Default: **ic2** when using incontrol2 api. **device** when using device api.)

<!--
## Running in Docker

```bash
docker build --tag dylanve151/PeplinkAPI .
docker run -d dylanve151/PeplinkAPI
```

-->
