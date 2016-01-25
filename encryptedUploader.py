import os,sys,gnupg,time
from datetime import datetime
import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client.file import Storage
from googleapiclient.http import MediaFileUpload
import logging

class encryptedUploader:
    def __init__(self):
       self.source = os.path.normpath(sys.argv[1])
       self.remote = os.path.normpath(sys.argv[2])
       self.oauth_folder = os.path.normpath(sys.argv[3])
       self.encrypted = "/tmp"
       self._create_drive()

    def run(self):
        print "test"
        self._encryptDir(self.source,self.remote)

#need to create new drive folders of mime type google.folder thing
#parenting correctly with their ID number
    def _encryptDir(self,source,remote):
        gpg = gnupg.GPG()
        key_data = open('backup_pub.gpg').read()
        import_result = gpg.import_keys(key_data)
        print(import_result.results)
        fingerprint = '0402C9ADB9626A45700A39F0663890816CDA1490'
        parent_folder_id =[]
        parent_folder_id.insert(0,self._get_folder_id(remote))
        folder_response = self.drive_service.files().list(q="title='%s' and mimeType contains 'application/vnd.google-apps.folder' and trashed=false" % remote).execute()
        folders = folder_response['items']
        files_response = self.drive_service.files().list(q="title='%s' and mimeType contains 'video/avi' and trashed=false" % remote).execute() 
        files_remote = files_response['items']
        print "folders " + str(folders) +" files " +str(files_remote)
        for root, dirs, files in os.walk(source, topdown=True):           
            print root
            subdir = os.path.relpath(root,self.source)
            remote_path = os.path.join(remote,subdir)
            print remote_path
            if not remote_path in folders:
                print 'folder is not in remote'
                current_id = self.make_folder(root,parent_folder_id[0])
                parent_folder_id.insert(0,current_id)
            for name in files:
                file_path = os.path.join(root, name)
                subdir = os.path.relpath(root,self.source)
                newpath = os.path.join(self.encrypted,subdir)
                encrypted_path = os.path.join(newpath,name)                
                statinfo = os.stat(file_path)
                remote_path = os.path.join(remote,subdir)
                remote_path = os.path.join(remote_path,name)
                        
                if statinfo.st_size<100000000 and name != '.':
                    with open(file_path, 'rb') as f:
                        if(not name+".gpg" in files_remote):
                            print "file not in remote "+remote_path+".gpg"
                        messsage = str(gpg.encrypt(f.read(),fingerprint,output=encrypted_path+".gpg"))
                        self.upload_file(encrypted_path+'.gpg',parent_folder_id[0])
            if(len(parent_folder_id)>0):
                parent_folder_id.pop();
    def _create_drive(self):
        """Create a Drive service."""
        auth_required = True
        #Have we got some credentials already?
        storage = Storage(self.oauth_folder+'/uploader_credentials.txt')    
        credentials = storage.get()
        try:
            if credentials:
                # Check for expiry
                if credentials.access_token_expired:
                    if credentials.refresh_token is not None:
                        credentials.refresh(httplib2.Http())
                        auth_required = False
                else:
                    auth_required = False
                
        except:
            print "Something went wrong - try manual auth"
            pass
                        
        if auth_required:
            flow = client.flow_from_clientsecrets(
                self.oauth_folder+'/client_secrets.json',
                scope='https://www.googleapis.com/drive',
                redirect_uri='urn:ietf:wg:oauth:2.0:oob')
            auth_uri = flow.step1_get_authorize_url()

            print 'Go to this link in your browser:'
            print auth_uri

            auth_code = raw_input('Enter the auth code: ')
            credentials = flow.step2_exchange(auth_code)
            storage.put(credentials)

        #Get the drive service
        http_auth = credentials.authorize(httplib2.Http())
        self.drive_service = discovery.build('drive', 'v2', http_auth)
            
    def _get_folder_id(self, folder_name):
        """Find and return the id of the folder given the title."""
        files = self.drive_service.files().list(q="title='%s' and mimeType contains 'application/vnd.google-apps.folder' and trashed=false" % folder_name).execute()
        if len(files['items']) == 1:
            folder_id = files['items'][0]['id']
            return folder_id
        else:
            return "folder not found"

    def make_folder(self,path,parent_id):
        file_metadata = {
            'title' : str(os.path.basename(path)),
            'parents' : [{'id':parent_id}],
            'mimeType' : 'application/vnd.google-apps.folder'
        }
        file = self.drive_service.files().insert(body=file_metadata,fields='id').execute()
        return file.get('id')

    def upload_file(self, file_path,parent='root'):
        folder_id = self._get_folder_id(parent)
        
        media = MediaFileUpload(file_path, mimetype='video/avi')
        response = self.drive_service.files().insert(media_body=media, body={'title':os.path.basename(file_path), 'parents':[{u'id': folder_id,"kind": "drive#fileLink"}]}).execute()
        #print response
        video_link = response['alternateLink']
        
        if self.delete_after_upload:
            os.remove(file_path)    

if __name__ == "__main__":
    if len(sys.argv)<4:
        print "more arguments required. Must include: source directory,remote (Google Drive) directory, and oauth storage directory"
        exit()
    uploader = encryptedUploader()
    uploader.run()
