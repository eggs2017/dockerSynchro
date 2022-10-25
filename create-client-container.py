import os
import argparse

#build .env file
#SSH_USER, SSH_PASS, SSH_PORT

#default values
defaultPort = '422'
defaultUser = 'rsync_u'
defaultDir = '/SynchBackupDir'
defaultMode = '@daily'

parser = argparse.ArgumentParser(description='Create rsync client container')

parser.add_argument('con_name', action='store'      , help='container name')
parser.add_argument('server_host', action='store'   , help='server host ip')
parser.add_argument('synch_dir', action='store'     , help='local directory to synchro e.g \'/c/dirA\' or \'/d/DirA\'')
parser.add_argument('ssh_pass' , action='store'     , help='ssh password')

parser.add_argument('--cron_mode'   , action='store', default='{0}'.format(defaultMode),    help='crontab mode e.g \'@daily\', \'@hourly\', \'@weekly\' or just \'0 2 * * *\', default value \'{0}\''.format(defaultMode))
parser.add_argument('--ssh_port'    , action='store', default='{0}'.format(defaultPort),    help='ssh port, default value \'{0}\''.format(defaultPort))
parser.add_argument('--ssh_user'    , action='store', default='{0}'.format(defaultUser),    help='ssh user, default value \'{0}\''.format(defaultUser))
parser.add_argument('--server_synch_dir', action='store',default='{0}'.format(defaultDir),  help='server storage path, default value \'{0}\''.format(defaultDir))

# Execute the parse_args() method
args = parser.parse_args()
dictArgs = vars(args)
print(dictArgs)


#save
configDir = './config'
if not os.path.exists(configDir):
    os.makedirs(configDir)
f = open('{0}/.envClient'.format(configDir), 'w', newline='\n')

print('COMPOSE_PROJECT_NAME=synchro-{0}'.format(dictArgs['con_name']), sep='\n', file=f)
print('CON_NAME={0}'.format(dictArgs['con_name']), sep='\n', file=f)

print('SERVER_HOST={0}'.format(dictArgs['server_host']), sep='\n', file=f)
print('SERVER_SYNCH_DIR={0}'.format(dictArgs['server_synch_dir']), sep='\n', file=f)

print('SYNCH_DIR={0}'.format(dictArgs['synch_dir']), sep='\n', file=f)
print('CRON_MODE={0}'.format(dictArgs['cron_mode']), sep='\n', file=f)

print('SSH_USER={0}'.format(dictArgs['ssh_user']), sep='\n', file=f)
print('SSH_PASS={0}'.format(dictArgs['ssh_pass']), sep='\n', file=f)
print('SSH_PORT={0}'.format(dictArgs['ssh_port']), sep='\n', file=f)
f.close() 

#create ssh_user.pass file

f = open('./client_alpine/ssh_user.pass', 'w')
f.write(dictArgs['ssh_pass'])
f.close()

#update template
synchDirs = dictArgs['synch_dir'].split(':')
volumesVal = ''
cronVal = ''

for synchDir in synchDirs:
    destDir = synchDir.replace('/', '_')
    volumeVal = '{0}:/mnt/{1}:ro'.format(synchDir,destDir)
    volumesVal += '         - {0} \n'.format(volumeVal)
    
    cronVal += "{0} /synchDir.sh '{1}' '{2}' '{3}'>> /var/log/cron.log 2>&1 \n".format(
            dictArgs['cron_mode'], 
            volumeVal.split(':')[1], 
            dictArgs['server_synch_dir'],
            dictArgs['server_host'])

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
os.system("docker compose -f docker-compose-client-mod.yml --env-file ./config/.envClient build --no-cache ") 
os.system("docker compose -f docker-compose-client-mod.yml --env-file ./config/.envClient up -d --force-recreate")
