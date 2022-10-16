import os
import argparse

#build .env file
#SSH_USER, SSH_PASS, SSH_PORT
parser = argparse.ArgumentParser(description='Create rsync client container')

parser.add_argument('CON_NAME', action='store', help='container name')

parser.add_argument('SERVER_HOST', action='store', help='server host')
parser.add_argument('SYNCH_DIR', action='store', help='local directory to synchro e.g /c/dirA or /d/DirA')
parser.add_argument('CRON_MODE', action='store', help='crontab mode e.g @daily, @hourly, @weekly or just 0 2 * * *')

#TODO Check if /config/.envServer exists then use defined variables or set predefined

parser.add_argument('--SSH_PORT', action='store', default='422', help='ssh port')
parser.add_argument('--SSH_USER', action='store', default='rsync_u', help='ssh user')
parser.add_argument('--SSH_PASS', action='store',default='rsync_u_gglhguylkguflshfsdhfsuf', help='ssh password')

parser.add_argument('--SERVER_SYNCH_DIR', action='store',default='/SynchBackupDir', help='server storage path')

# Execute the parse_args() method
args = parser.parse_args()
dictArgs = vars(args)
print(dictArgs)


#save
configDir = './config'
if not os.path.exists(configDir):
    os.makedirs(configDir)
f = open('{0}/.envClient'.format(configDir), 'w', newline='\n')

print('COMPOSE_PROJECT_NAME=project-{0}'.format(dictArgs['CON_NAME']), sep='\n', file=f)
print('CON_NAME={0}'.format(dictArgs['CON_NAME']), sep='\n', file=f)

print('SERVER_HOST={0}'.format(dictArgs['SERVER_HOST']), sep='\n', file=f)
print('SERVER_SYNCH_DIR={0}'.format(dictArgs['SERVER_SYNCH_DIR']), sep='\n', file=f)

print('SYNCH_DIR={0}'.format(dictArgs['SYNCH_DIR']), sep='\n', file=f)
print('CRON_MODE={0}'.format(dictArgs['CRON_MODE']), sep='\n', file=f)

print('SSH_USER={0}'.format(dictArgs['SSH_USER']), sep='\n', file=f)
print('SSH_PASS={0}'.format(dictArgs['SSH_PASS']), sep='\n', file=f)
print('SSH_PORT={0}'.format(dictArgs['SSH_PORT']), sep='\n', file=f)
f.close() 

#create ssh_user.pass file

f = open('./client_alpine/ssh_user.pass', 'w')
f.write(dictArgs['SSH_PASS'])
f.close()

#update template
synchDirs = dictArgs['SYNCH_DIR'].split(':')
volumesVal = ''
cronVal = ''

for synchDir in synchDirs:
    destDir = synchDir.replace('/', '_')
    volumeVal = '{0}:/mnt/{1}:ro'.format(synchDir,destDir)
    volumesVal += '         - {0} \n'.format(volumeVal)
    
    cronVal += "{0} /synchDir.sh {1} {2} >> /var/log/cron.log 2>&1 \n".format(
            dictArgs['CRON_MODE'], 
            volumeVal.split(':')[1], 
            dictArgs['SERVER_SYNCH_DIR'])

with open('docker-compose-template-client.yml') as f:
    updatedTemplate=f.read().replace('${VOLUMES}', volumesVal)

with open('docker-compose-client-mod.yml', "w") as f:
    f.write(updatedTemplate)

f.close()

#create scheduler_rsync.txt for crontab
f = open('./client_alpine/scheduler_rsync.txt', 'w', newline='\n')
f.write(cronVal)
f.close()


#run command to build container  
os.system("docker-compose -f docker-compose-client-mod.yml --env-file ./config/.envClient build --no-cache ") 
os.system("docker-compose -f docker-compose-client-mod.yml --env-file ./config/.envClient up -d --force-recreate")
