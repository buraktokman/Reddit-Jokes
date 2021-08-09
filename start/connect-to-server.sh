#!/usr/local/bin/bash

#
#	CONNECT SCREEN SESSION RUNNING WEB_APP
#

USERNAME=''
IPADDRESS=''
PASSWORD=''

# Connect via SSH to server
sshpass -p $PASSWORD ssh -o StrictHostKeyChecking=no $USERNAME@$IPADDRESS -t screen -r WEB_APP # -i $PKEY

# Connect to screen - Attach
# screen -r WEB_APP

# CTRL+A - D -> Detach