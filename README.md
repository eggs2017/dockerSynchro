Python scripts generates containers server and client side to synchronize directory (make backups)
Both containers are based on alpine linux.
Server container have ssh server and rsync tools installed and running.
Client container connect periodically to certain server container in specific period of time to synchronise using ssh & rsync tools.


usage: create-server-container.py [-h] [--SSH_USER] [--SSH_PASS] [--SSH_PORT] CON_NAME <br />

**Create rsync server container**

positional arguments:<br />
  CON_NAME     container name <br />

optional arguments:<br />
  -h, --help   show this help message and exit <br />
  --SSH_USER   ssh user <br />
  --SSH_PASS   ssh password <br />
  --SSH_PORT   ssh server port <br />

usage: create-client-container.py [-h] [--SSH_PORT] [--SSH_USER] [--SSH_PASS] [--SERVER_SYNCH_DIR] CON_NAME SERVER_HOST SYNCH_DIR CRON_MODE

**Create rsync client container**

positional arguments:<br />
  CON_NAME      container name <br />
  SERVER_HOST   server host <br />
  SYNCH_DIR     local directory to synchro e.g /c/dirA or /d/DirA <br />
  CRON_MODE     crontab mode e.g @daily, @hourly, @weekly or just 0 2 * * * <br />

optional arguments: <br />
  -h, --help            show this help message and exit <br />
  --SSH_PORT    ssh port <br />
  --SSH_USER    ssh user <br />
  --SSH_PASS    ssh password <br />
  --SERVER_SYNCH_DIR  server storage path <br />
  

**Example of using:**

1. Create server container on machine with linux ip 172.16.0.10

  python create-server-container.py  backupServer  <br />

  **docker container has been created with following params:  <br />**
    {'CON_NAME': 'backupServer', 'SSH_USER': 'rsync_u', 'SSH_PASS': 'jlvu6MAzXwEzYkjerbxu', 'SSH_PORT': '422'}  <br />
    
2. copy generated password value to clipboard and use it in p.3.

3. Create client container on windows machine to backup every 1 hour directory c:\storage  <br />
  
  python create-client-container.py 'storage-con' '172.16.0.10' '/c/storage1' '@hourly' --SSH-PASS='jlvu6MAzXwEzYkjerbxu' <br />
  
  **docker container has been created on client machine and now every 1 hour directory is synchronized to server created in p.1**
  
