import os, gnupg, time, ConfigParser

class encrypt:
        def __init__(self):
                self.gpg = gnupg.GPG()
                self.key_data = open('backup_key.asc').read()
                self.import_result = self.gpg.import_keys(self.key_data)
                print(self.import_result.results)
                config = ConfigParser.SafeConfigParser()
                config.read('options.conf')
                self.fingerprint = config.get('gpg','fingerprint',1)
                self.encrypted = config.get('folder','temp',1)
        
        def encrypt(self,file_path):
                print file_path
                newpath = os.path.basename(file_path)
                encrypted_path = os.path.join(self.encrypted,newpath)
                statinfo = os.stat(file_path)
                if statinfo.st_size<100000000:
                        with open(file_path, 'rb') as f:
                                message = str(self.gpg.encrypt(f.read(),self.fingerprint,output=encrypted_path+'.gpg'))
                                return (encrypted_path+'.gpg')

