#!/bin/sh

# Start the run once job.
echo "Docker container has been started - CRON service"

#declare -p | grep -Ev 'BASHOPTS|BASH_VERSINFO|EUID|PPID|SHELLOPTS|UID' > /container.env

# Setup a cron schedule --setup this !!
#echo "SHELL=/bin/bash
#BASH_ENV=/container.env
#@hourly /synchDir.sh '/mnt/c/MK'     >> /var/log/cron.log 2>&1
#@daily  /synchDir.sh '/mnt/c/Ultra'  >> /var/log/cron.log 2>&1
#This extra line makes it a valid cron ORG" > scheduler.txt

crontab scheduler_rsync.txt
#cron -f
/usr/sbin/crond -f -l 8
# Execute the CMD from the Dockerfile:
#exec "$@"