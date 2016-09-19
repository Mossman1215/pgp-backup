from __future__ import print_function
import httplib2,os
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from googleapiclient.http import MediaFileUpload

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

#if scope is modified new credentials must be made
SCOPE = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = '/home/moss/oauth/client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir,'oauth')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,'credentials.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE,SCOPE)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow,store,flags)
        else:
            credentials = tools.run(flow,store)
        print('Storing credentials to ' + credential_path)
    return credentials
def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive','v3',http=http)
    results = service.files().list(
        pageSize=10,fields="nextPageToken, files(id,name)").execute()
    items = results.get('files',[])
    if not items:
        print('No files found')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'],item['id']))
    print('find all folders query')
    result_set = service.files().list(pageSize=10,fields="nextPageToken, files(id,name)",q="name={0} and mimeType contains 'application/vnd.google-apps.folder' and trashed=false").execute()
    print('the keys of the result set')
    print(result_set.keys())
    print('uploading a file')
    file_path = '/home/moss/Documents/derp.org'
    media = MediaFileUpload(file_path, mimetype='text/plain')
    body= {'name':os.path.basename(file_path)}
    response = service.files().create(body=body,media_body=media).execute()
    print('upload complete')
    print('resulting response:')
    print(str(response))
    print('creating a folder')
    file_metadata = {
        'name' : 'test',
        'mimeType' : 'application/vnd.google-apps.folder'
    }
    response = service.files().create(body=file_metadata).execute()
    print("request executed")
    print('response')
    print(str(response))

if __name__=='__main__':
    main()
