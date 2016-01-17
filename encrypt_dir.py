import sys
import os
import gnupg
import time
if(len(sys.argv)<4):
	print "not enough arguments"
        print "must have <source> <encrypted> <remote> directories"
	exit()
source = os.path.normpath(sys.argv[1])
encrypted = os.path.normpath(sys.argv[2])
remote = os.path.normpath(sys.argv[3])
gpg = gnupg.GPG()
fingerprint = '0402C9ADB9626A45700A39F0663890816CDA1490'

for root, dirs, files in os.walk(source, topdown=True):           
    for name in dirs:
        newpath = os.path.join(root,name)
        if(not os.path.exists(newpath)):
            print 'path missing'
            os.makedirs(newpath)
            
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
                        message = str(gpg.encrypt(f.read(),fingerprint,output=encrypted_path))
        print 'file done'
        
print 'All Done!'
command = "cp -r "+encrypted+"/ "+remote
print "command "+command
result = ""
resulterror = ""
#print subprocess.call(command,stdout=result,stderr=resulterror)
print 'synched'
