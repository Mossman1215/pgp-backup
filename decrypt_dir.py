import sys
import os
import gnupg
if(len(sys.argv)<4):
	print "not enough arguments"
        print "must have <source> <decrypted> directories and <passphrase>"
	exit()
source = os.path.normpath(sys.argv[1])
decrypted = os.path.normpath(sys.argv[2])
password = sys.argv[3]
gpg = gnupg.GPG(homedir='/home/gdrive/gpghome')


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
        newpath = os.path.join(decrypted,newpath)
        decrypted_path = os.path.join(newpath,name)
        if(not os.path.exists(newpath)):
            os.makedirs(newpath)
            print 'built path'
        with open(file_path, 'rb') as f:
                message = str(gpg.decrypt_file(f,passphrase=password,output=decrypted_path))
        print 'file done'
        
print 'All Done!'
