import os
import random
import argparse
import string 

def rand_pass(size): 
        
    # Takes random choices from 
    # ascii_letters and digits 
    generate_pass = ''.join([random.choice( string.ascii_uppercase + 
                                            string.ascii_lowercase + 
                                            string.digits) 
                                            for n in range(size)]) 
                            
    return generate_pass 


#build .env file
#SSH_USER, SSH_PASS, SSH_PORT
parser = argparse.ArgumentParser(description='Create rsync server container')

# Add the arguments
parser.add_argument('CON_NAME', action='store', help='container name')

parser.add_argument('-SSH_USER', action='store', default='rsync_u', help='ssh user, default value \'rsync_u\'')

rpv = rand_pass(20)
parser.add_argument('-SSH_PASS', action='store',default='{0}'.format(rpv),  help='ssh password, defaulted by \'{0}\''.format(rpv))
parser.add_argument('-SSH_PORT', action='store',default='422',              help='ssh server port, default value \'422\'')


# Execute the parse_args() method
args = parser.parse_args()
dictArgs = vars(args)
print(dictArgs)

#save
configDir = './config'
if not os.path.exists(configDir):
    os.makedirs(configDir)
f = open('{0}/.envServer'.format(configDir), 'w', newline='\n')

print('CON_NAME={0}'.format(dictArgs['CON_NAME']), sep='\n', file=f)
print('SSH_USER={0}'.format(dictArgs['SSH_USER']), sep='\n', file=f)
print('SSH_PASS={0}'.format(dictArgs['SSH_PASS']), sep='\n', file=f)
print('SSH_PORT={0}'.format(dictArgs['SSH_PORT']), sep='\n', file=f)
f.close() 

#run command to build container  
os.system("docker-compose -f docker-compose-template-server.yml --env-file ./config/.envServer build --no-cache ") 
os.system("docker-compose -f docker-compose-template-server.yml --env-file ./config/.envServer up -d --force-recreate")