import gnupg

gpg = gnupg.GPG(homedir='/home/gdrive/gpghome')
key_data = open('backup_pub.gpg').read()
import_result = gpg.import_keys(key_data)
print(import_result.results)
print "done"
