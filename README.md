Automatics docker containers server & clients side  generator to backup directories.

Both docker containers are based on alpine linux.

Server container have ssh server and rsync tools installed and running.
Each client container connects periodically to certain server container in specific period of time to backup directories using ssh & rsync tools.<br />

Command using to synchronization: </br>

```
rsync -arv
-a, --archive  
-r, --recursive 
-v, --verbose   
 ```

The purpose of this project:
  "I was wondering about an effective method to backup important data (my laptop and other computers at home) in safe place. No native solution met my expectations, and I didn't want to use commercial or highly complex systems."
  
**Create rsync server container**

Usage: ```python create-server-container.py [-h] [-ssh_user SSH_USER] [-ssh_pass SSH_PASS] [-ssh_port SSH_PORT] con_name ```

```
positional arguments:
  con_name            container name

optional arguments:
  -h, --help          show this help message and exit
  -ssh_user SSH_USER  ssh user, default value 'rsync_u'
  -ssh_pass SSH_PASS  ssh password, defaulted by 'pDTdPBBxnr9465kjKxgw'
  -ssh_port SSH_PORT  ssh server port, default value '422'
```

**Create rsync client container**

Usage: ```python create-client-container.py [-h] [--cron_mode CRON_MODE] [--ssh_port SSH_PORT] [--ssh_user SSH_USER] [--server_synch_dir SERVER_SYNCH_DIR] con_name server_host synch_dir ssh_pass```

```
positional arguments:
  con_name              container name
  server_host           server host ip
  synch_dir             local directory to synchro e.g '/c/dirA' or '/d/DirA'
  ssh_pass              ssh password

optional arguments:
  -h, --help            show this help message and exit
  --cron_mode CRON_MODE
                        crontab mode e.g '@daily', '@hourly', '@weekly' or just '0 2 * * *', default value '@daily'
  --ssh_port SSH_PORT   ssh port, default value '422'
  --ssh_user SSH_USER   ssh user, default value 'rsync_u'
  --server_synch_dir SERVER_SYNCH_DIR
                        server storage path, default value '/SynchBackupDir'
 ``` 

**Example of using:**

1. Create server container.

  ```python create-server-container.py  'backupServer'  ```<br />

  **docker container has been created with following params:  <br />**
    {'CON_NAME': 'backupServer', 'SSH_USER': 'rsync_u', 'SSH_PASS': 'jlvu6MAzXwEzYkjerbxu', 'SSH_PORT': '422'}  <br />
    
2. Copy password using clipboard and create client, ip of server is required.<br />
  
  ```python create-client-container.py 'storage-con' '172.16.0.10' '/c/storage1' 'jlvu6MAzXwEzYkjerbxu' ```
  
  **docker container has been created on client machine and now every 1 hour directory is synchronized to the server side**

Note: There is option to make multiple directory backup. </br>

  In following case system synchronise c:\dirA, c:\dirB , c:\dirC  <br />

  ```python create-client-container.py 'storage-con' '172.16.0.10' '/c/dirA:/c/dirB:/c/dirC' 'jlvu6MAzXwEzYkjerbxu' ```

```
 Backup directories on server side 

      '/SynchBackupDir/_c_dirA' 
      '/SynchBackupDir/_c_dirB' 
      '/SynchBackupDir/_c_dirC' 
 ``` 

**Second example**

What if want You to be even safer and backup Your data in multiple places in parallel? </br>

1. Open client docker container in shell </br>
  ```docker -exec  -it [container id] /bin/sh```

2. Edit crontab file </br>
      ```crontab -e```

    Can looks like below </br>

      ```
      @hourly /synchDir.sh '/mnt/_c_dirA' '/SynchBackupDir' '192.168.0.10'>> /var/log/cron.log 2>&1 
      @hourly /synchDir.sh '/mnt/_c_dirB '/SynchBackupDir' '192.168.0.10'>> /var/log/cron.log 2>&1 
      ```
     Change to: </br>
    
     ```
     serverA='192.168.0.10'
     serverB='192.168.0.11'

     @hourly /synchDir.sh '/mnt/_c_dirA' '/SynchBackupDir' $serverA >> /var/log/cron.log 2>&1 
     @hourly /synchDir.sh '/mnt/_c_dirB  '/SynchBackupDir' $serverA >> /var/log/cron.log 2>&1
     
     @hourly /synchDir.sh '/mnt/_c_dirA' '/SynchBackupDir' $serverB >> /var/log/cron.log 2>&1 
     @hourly /synchDir.sh '/mnt/_c_dirB  '/SynchBackupDir' $serverB >> /var/log/cron.log 2>&1 
    ```