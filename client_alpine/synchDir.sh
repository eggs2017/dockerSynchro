#!/bin/sh

synchDir="$1"
remoteDestDir="$2"
serverHost="$3"

ts=$(date +%d-%m-%Y_%H-%M-%S)
echo "Synch Begin $ts" >> '/var/log/synch.log'
echo "synchronization of $synchDir" >> '/var/log/synch.log'
#exec
rsync -arv -e "sshpass -f /ssh_user.pass ssh -o StrictHostKeyChecking=no -p $server_port" \
    --progress "$synchDir" $ssh_user@$serverHost:"$remoteDestDir"

timeStstamp=$(date +%d-%m-%Y_%H-%M-%S)
echo "Synch End $ts" >> '/var/log/synch.log'
