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
       self._create_drive()
       self.mapping = dict()

    def run(self):
        self.upload_dir()
    
    def getParentID(self,filename):
        #search the dictionary for the filename
        if(filename in self.mapping):
            return self.mapping[filename]
        else:
            return -1
            
    def upload_dir(self):
        #upload the source folder here
        print(self.number_of_operations())
        for root,subdirs,files in os.walk(self.source, topdown=True):
            #store the root id
            name = os.path.basename(root)
            pID = self.getParentID(name)
            if(pID == -1):
                pID = self.get_folder_id(self.remote)#add error code if folder does not exist make it! or crash with helpfull message
                self.mapping[name] = pID
            identifier = self.make_folder(name,pID)
            for subdir in subdirs:
                subName = os.path.basename(subdir)
                self.mapping[subName] = identifier
            for fi in files:
                file_path = os.path.join(root,fi)
                print(file_path)
                self.upload_file(file_path,identifier)
    
    def number_of_operations(self):
        count = 0
        for root,subdirs,files in os.walk(self.source, topdown=True):
            count+=1
            count= count + len(files)
        return count
    
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
                scope='https://www.googleapis.com/auth/drive',
                redirect_uri='urn:ietf:wg:oauth:2.0:oob')
            auth_uri = flow.step1_get_authorize_url()

            print 'Go to this link in your browser:'
            print auth_uri

            auth_code = raw_input('Enter the auth code: ')
            credentials = flow.step2_exchange(auth_code)
            storage.put(credentials)

        #Get the drive service
        http_auth = credentials.authorize(httplib2.Http())
        self.drive_service = discovery.build('drive', 'v3', http_auth)
            
    def get_folder_id(self, folder_name):
        """Find and return the id of the folder given the name."""
        resp = self.drive_service.files().list(fields='nextPageToken,files(id)',
                                               q="name='{0}' and mimeType contains 'application/vnd.google-apps.folder' and trashed=false".format(folder_name)).execute()
        files = resp.get('files',[])
        if len(files) == 1:
            folder_id = files[0]['id']
            return folder_id
        else:
            return "folder not found"

    def make_folder(self,name,parent_id):
        file_metadata = {
            'name' : name,
            'parents' : [{'id':parent_id}],
            'mimeType' : 'application/vnd.google-apps.folder'
        }
        file = self.drive_service.files().create(body=file_metadata,fields='id').execute()
        return file.get('id')

    def upload_file(self, file_path,parent):
        #folder_id = self._get_folder_id(parent)
        try:
            media = MediaFileUpload(file_path, mimetype='text/plain')
            response = self.drive_service.files().create(media_body=media, body={'name':os.path.basename(file_path), 'parents':[{u'id': parent}]}).execute()
            #print response
            #video_link = response['alternateLink']
            #if self.delete_after_upload:
            #os.remove(file_path)
        except TypeError as e:
            print("type error "+str(e))

if __name__ == "__main__":
    if len(sys.argv)<4:
        print "more arguments required. Must include: source directory,remote (Google Drive) directory, and oauth storage directory"
        exit()
    uploader = encryptedUploader()
    uploader.run()
