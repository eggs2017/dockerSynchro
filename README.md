```markdown
# Data Backup Tool for Sensitive Information

This tool utilizes Docker containers to create secure, server-client setups specifically designed for backing up sensitive data. Both the server and client containers are based on Alpine Linux 3.16. The server container includes an SSH server and rsync tools for secure data synchronization. Each client container periodically connects to a specific server container to backup directories using SSH and rsync.

The command used for synchronization is:

```bash
rsync -arv
-a, --archive  
-r, --recursive 
-v, --verbose   
```

## Project Overview:
The primary goal of this project was to find an effective method for backing up important data (laptop and home computers) to a secure location. No native solutions met the user's expectations, and using commercial or highly complex systems was not desired.

## Creating an rsync Server Container:
Usage: 
```python
python create-server-container.py [-h] [-ssh_user SSH_USER] [-ssh_pass SSH_PASS] [-ssh_port SSH_PORT] con_name
```
Default values are specified for some parameters, e.g., `ssh_password` is defaulted to 'pDTdPBBxnr9465kjKxgw' and `ssh_port` is defaulted to '422'.

## Creating an rsync Client Container:
Usage: 
```python
python create-client-container.py [-h] [--cron_mode CRON_MODE] [--ssh_port SSH_PORT] [--ssh_user SSH_USER] [--server_synch_dir SERVER_SYNCH_DIR] con_name server_host synch_dir ssh_pass
```
The `--cron_mode` parameter specifies the synchronization frequency (e.g., '@daily', '@hourly', '@weekly', or '0 2 * * *'). The default value is '@daily'.

## Example Usage:

1. Create a server container on the server machine:

```bash
python create-server-container.py 'backupServer'
```

This command creates a Docker container with the specified parameters (e.g., `con_name`, `ssh_user`, and `ssh_pass`).

2. On the client machine, copy the password to the clipboard and run:

```bash
python create-client-container.py 'storage-multi-dirs' '192.168.0.10' '/c/storage1' 'jlvu6MAzXwEzYkjerbxu'
```

This creates a client container that will synchronize the specified directory with the server every hour by default.

## Support for Multiple Directories:
To backup multiple directories simultaneously, use the following command:

```bash
python create-client-container.py 'storage-con' '192.168.0.10' '/c/dirA:/c/dirB:/c/dirC' 'jlvu6MAzXwEzYkjerbxu'
```

Backups of these directories will be stored on the server in separate locations (e.g., '/SynchBackupDir/_c\_dirA', '/SynchBackupDir/_c\_dirB', '/SynchBackupDir/_c\_dirC').

## Advanced Usage: Parallel Backups to Multiple Locations

1. Open a client Docker container in the shell:
```bash
docker -exec  -it [container id] /bin/sh
```

2. Edit the crontab file (e.g., `crontab -e`) and add synchronization commands for each target location, such as:
```bash
@daily /synchDir.sh '/mnt/_c\_dirA' '/SynchBackupDir' $serverContainerA >> /var/log/cron.log 2>&1 
@daily /synchDir.sh '/mnt/_c\_dirB' '/SynchBackupDir' $serverContainerA >> /var/log/cron.log 2>&1 
```
In this example, `$serverContainerA` represents the IP address of the source server for a given backup.

## Summary:
This data backup tool offers flexible and secure solutions for various synchronization scenarios, tailored to meet your specific needs. By utilizing Docker containers and rsync for secure data transfer, it ensures efficient and reliable backups of sensitive information.
```
