import os,sys,gnupg,time,ConfigParser
from datetime import datetime
import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client.file import Storage
from googleapiclient.http import MediaFileUpload
from encrypt import encrypt
from types import *
import logging

class EncryptedUploader:
    def __init__(self):
        config = ConfigParser.SafeConfigParser()
        config.read(os.path.normpath(sys.argv[3]))
        self.source = os.path.normpath(sys.argv[1])
        self.remote = os.path.normpath(sys.argv[2])
        self.oauth_folder = os.path.normpath(config.get('folder','oauth',1))
        #self.log_file = open(str(os.path.join(os.path.normpath(config.get('folder','log',1)),'EncryptedUploader.log')),'w')
        self._create_drive()
        self.mapping = dict()#names of directories to parent folder id
        self.encrypter = encrypt()
    def run(self):
        self.upload_dir()
    
    def getParentID(self,filename):
        #search the dictionary for the filename
        if(filename in self.mapping):
            return self.mapping[filename]
        else:
            return -1
            
    def upload_dir(self):
        print(self.number_of_operations())
        for root,subdirs,files in os.walk(self.source, topdown=True):
            title = os.path.basename(root)
            pID = self.getParentID(title)
            if(pID == -1):
                pID = self.get_folder_id(self.remote)#add error code if folder does not exist make it! or crash with helpfull message
                self.mapping[title] = pID
            identifier = self.make_folder(title,pID)
            for subdir in subdirs:
                subName = os.path.basename(subdir)
                self.mapping[subName] = identifier
            for fi in files:
                file_path = os.path.join(root,fi)
                print(file_path)
                #encrypt
                temporary_name = self.encrypter.encrypt(file_path)
                try:
                    result = self.upload_file(temporary_name,identifier)
                    if(type(result) is StringType): #will print error if upload fails
                        print(result)
                except TypeError as arg:
                    print("file type error (none): " + str(arg))
                time.sleep(1)
                os.remove(temporary_name)
    
    def number_of_operations(self):
        count = 0
        for root,subdirs,files in os.walk(self.source, topdown=True):
            count+=1
            count= count + len(files)
        return count
    
    def _create_drive(self):
        #"""Create a Drive service."""
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
        self.drive_service = discovery.build('drive', 'v2', http_auth)
            
    def get_folder_id(self, folder_name):
        #"""Find and return the id of the folder given the title."""
        files = self.drive_service.files().list(q="title='%s' and mimeType contains 'application/vnd.google-apps.folder' and trashed=false" % folder_name).execute()
        if len(files['items']) == 1:
            folder_id = files['items'][0]['id']
            return folder_id
        else:
            return "folder not found"

    def make_folder(self,title,parent_id):
        file_metadata = {
            'title' : title,
            'parents' : [{'id':parent_id}],
            'mimeType' : 'application/vnd.google-apps.folder'
        }
        file = self.drive_service.files().insert(body=file_metadata,fields='id').execute()
        return file.get('id')

    def upload_file(self, file_path,parent):
        media = MediaFileUpload(file_path, mimetype='video/avi')
        count = 0
        while(count < 3):
            try:
                response = self.drive_service.files().insert(media_body=media, body={'title':os.path.basename(file_path), 'parents':[{u'id': parent}]}).execute()
                return True
            except IOError as e:
                sleep(3)
                count+=1
        return "failure to upload: "+file_path
        #print response
        video_link = response['alternateLink']

if __name__ == "__main__":
    if len(sys.argv)!=4:
        print "arguments given were incorrect they must include: source directory,remote (Google Drive) directory, and configuration location"
        exit()
    uploader = EncryptedUploader()
    uploader.run()
