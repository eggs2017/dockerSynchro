#!/bin/sh

synchDir="$1"

ts=$(date +%d-%m-%Y_%H-%M-%S)
echo "Synch Begin $ts" >> '/var/log/synch.log'
echo "synchronization of $synchDir" >> '/var/log/synch.log'
#exec
rsync -arv -e "sshpass -f ssh_user.pass ssh -o StrictHostKeyChecking=no -p $server_port" --progress "$synchDir" $ssh_user@$server_host:"$server_synch_dir/$HOSTNAME"

timeStstamp=$(date +%d-%m-%Y_%H-%M-%S)
echo "Synch End $ts" >> '/var/log/synch.log'
