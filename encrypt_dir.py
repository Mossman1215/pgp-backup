import sys
import os
import gnupg
import time
import encrypt

config = ConfigParser.SafeConfigParser()
config.read('options.conf')
encrypted = config.get('folder','temp',1)
crypto = encrypt()

for root, dirs, files in os.walk(source, topdown=True):           
    for name in files:
        file_path = os.path.join(root, name)
        newpath = os.path.relpath(root,filepath)
        newpath = os.path.join(encrypted,newpath)
        if(not os.path.exists(newpath)):
            os.makedirs(newpath)
        crypto.encrypt(file_path)
        
print 'All Done!'
#print subprocess.call(command,stdout=result,stderr=resulterror)
