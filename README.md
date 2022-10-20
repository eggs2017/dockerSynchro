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

Usage: ```create-server-container.py [-h] [--SSH_USER] [--SSH_PASS] [--SSH_PORT] CON_NAME ```

```
positional arguments:
  CON_NAME     container name

optional arguments:
  -h, --help   show this help message and exit 
  --SSH_USER   ssh user 
  --SSH_PASS   ssh password 
  --SSH_PORT   ssh server port 
```

**Create rsync client container**

Usage: ```create-client-container.py [-h] [--SSH_PORT] [--SSH_USER] [--SSH_PASS] [--SERVER_SYNCH_DIR] CON_NAME SERVER_HOST SYNCH_DIR CRON_MODE```

```
positional arguments:
  CON_NAME      container name 
  SERVER_HOST   server host
  SYNCH_DIR     local directory to synchro e.g /c/dirA or /d/DirA 
  CRON_MODE     crontab mode e.g @daily, @hourly, @weekly or just 0 2 * * * 

optional arguments: 
  -h, --help            show this help message and exit 
  --SSH_PORT    ssh port
  --SSH_USER    ssh user 
  --SSH_PASS    ssh password 
  --SERVER_SYNCH_DIR  server storage path 
 ``` 

**Example of using:**

1. Create server container.

  ```python create-server-container.py  'backupServer'  ```<br />

  **docker container has been created with following params:  <br />**
    {'CON_NAME': 'backupServer', 'SSH_USER': 'rsync_u', 'SSH_PASS': 'jlvu6MAzXwEzYkjerbxu', 'SSH_PORT': '422'}  <br />
    
2. Copy password using clipboard and create client, ip of server is required.<br />
  
  ```python create-client-container.py 'storage-con' '172.16.0.10' '/c/storage1' '@hourly' --SSH-PASS='jlvu6MAzXwEzYkjerbxu' ```
  
  **docker container has been created on client machine and now every 1 hour directory is synchronized to the server side**

Note: There is option to make multiple directory backup. </br>

  In following case system synchronise c:\dirA, c:\dirB , c:\dirC  <br />

  ```python create-client-container.py 'storage-con' '172.16.0.10' '/c/dirA:/c/dirB:/c/dirC' '@hourly' --SSH-PASS='jlvu6MAzXwEzYkjerbxu' ```

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
      @hourly /synchDir.sh '/mnt/_c_dirA' '/SynchBackupDir' '192.168.0.10' >> /var/log/cron.log 2>&1 
      @hourly /synchDir.sh '/mnt/_c_dirB  '/SynchBackupDir' '192.168.0.10' >> /var/log/cron.log 2>&1 
      ```
     Change to: </br>
    
     ```
     serverContainerA='192.168.0.10'
     serverContainerB='192.168.0.11'

     @hourly /synchDir.sh '/mnt/_c_dirA' '/SynchBackupDir' $serverContainerA >> /var/log/cron.log 2>&1 
     @hourly /synchDir.sh '/mnt/_c_dirB  '/SynchBackupDir' $serverContainerA >> /var/log/cron.log 2>&1
     
     @hourly /synchDir.sh '/mnt/_c_dirA' '/SynchBackupDir' $serverContainerB >> /var/log/cron.log 2>&1 
     @hourly /synchDir.sh '/mnt/_c_dirB  '/SynchBackupDir' $serverContainerB >> /var/log/cron.log 2>&1 
    ```
