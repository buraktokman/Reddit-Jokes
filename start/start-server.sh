#!/bin/bash

#
#	INITIATE WEB APP
#
PASSWD=''
IPADDRESS='0.0.0.0'
PORT='4000' # 443

# Script path
SCRIPT_PATH=""

cd $SCRIPT_PATH;

# Create screen
#screen -dmS WEB_APP bash -c "cd  $SCRIPT_PATH;sudo -S <<< $PASSWD gunicorn --timeout 90 --log-level=DEBUG --workers=$((2 * $(getconf _NPROCESSORS_ONLN) + 1)) -b $IPADDRESS:$PORT app:app"
screen -dmS WEB_APP bash -c "cd $SCRIPT_PATH;gunicorn --timeout 90 --log-level=DEBUG --workers=$((2 * $(getconf _NPROCESSORS_ONLN) + 1)) -b $IPADDRESS:$PORT app:app"

# --certfile ssl/public.pem --keyfile ssl/private.pem
# -w 8

# gunicorn --timeout 90 --log-level=DEBUG --workers=$((2 * $(getconf _NPROCESSORS_ONLN) + 1)) -b $IPADDRESS:$PORT app:app
# python3 $SCRIPT_PATH/app.py