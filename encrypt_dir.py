import sys
import os
import gnupg
import time
if(len(sys.argv)<2):
	print "not enough arguments"
        print "must have <source> directory"
	exit()
source = os.path.normpath(sys.argv[1])
gpg = gnupg.GPG()
key_data = open('backup_pub.gpg').read()
import_result = gpg.import_keys(key_data)
print(import_result.results)
fingerprint = '0402C9ADB9626A45700A39F0663890816CDA1490'
encrypted = '/tmp'

for root, dirs, files in os.walk(source, topdown=True):           
    for name in files:
        file_path = os.path.join(root, name)
        print file_path
        newpath = os.path.relpath(root,source)
        newpath = os.path.join(encrypted,newpath)
        encrypted_path = os.path.join(newpath,name)
        if(not os.path.exists(newpath)):
            os.makedirs(newpath)
            print 'built path'
        statinfo = os.stat(file_path)
        if statinfo.st_size<100000000:
                with open(file_path, 'rb') as f:
                        message = str(gpg.encrypt(f.read(),fingerprint,output=encrypted_path+'.gpg'))
                f.close()
        print 'file done'
        
print 'All Done!'
#print subprocess.call(command,stdout=result,stderr=resulterror)
print 'synched'
