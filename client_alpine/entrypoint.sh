#!/bin/sh

# Start the run once job.
echo "Docker container has been started - CRON service"

crontab scheduler_rsync.txt
#cron -f
/usr/sbin/crond -f -l 8
