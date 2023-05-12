# PeplinkAPI-Examples

## Running locally Bash on debian

```bash
sudo apt-get update
sudo apt-get install -y curl jq
```

Copy `.env.example` to `.env` and replace variables in the file

### Required IC2:
* client_id=
* client_secret=
* grant_type=**client_credentials** or **authorization_code** (Default: **client_credentials** (requires no interaction))

### Optional IC2:
* redirect_uri=For example: https://peplink.com (Only required when using **authorization_code** (requires interaction))
* server_type=**device** or **ic2** (Default: **ic2** when using incontrol2 api. **device** when using device api.)
* server_prefix=By default https://api.ic.peplink.com for use with https://incontrol2.peplink.com

### Required Device:
* client_id=
* client_secret=
* server_prefix=By default https://api.ic.peplink.com for use with https://incontrol2.peplink.com
* server_type=**device** or **ic2** (Default: **ic2** when using incontrol2 api. **device** when using device api.)

### Optional Device:
* admin_user=Admin username for webgui login. (Only needed for creating client ID + client secret.)
* admin_pass=Admin password for webhui login. (Only needed for creating client ID + client secret.)
* server_type=**device** or **ic2** (Default: **ic2** when using incontrol2 api. **device** when using device api.)

```bash
./bash/apitoken.bash
```

<!--
## Running locally Python

```bash
pip install 
```

Copy `.env.example` to `.env` and replace variables in the file
* client_id=
* client_secret=
* grant_type=**client_credentials** or **authorization_code** (Default: **client_credentials** (requires no interaction))

### Optional:

* redirect_uri=For example: https://peplink.com (Only required when using **authorization_code** (requires interaction))
* api_type=**device** or **ic2** (Default: **ic2** when using incontrol2 api. **device** when using device api.)
* server_prefix=By default https://api.ic.peplink.com for use with https://incontrol2.peplink.com

```bash
python ./python/apitoken.py
```


## Running in Docker

```bash
docker build --tag dylanve151/PeplinkAPI .
docker run -d dylanve151/PeplinkAPI
```
-->
