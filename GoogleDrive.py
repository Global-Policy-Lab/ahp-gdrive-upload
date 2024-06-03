import os
import sys

def set_project_root():
    """ Sets the root directory for the project dynamically. """
    root_dir = os.path.abspath(__file__)
    while not os.path.exists(os.path.join(root_dir, '.project_root')) and root_dir != '/':
        root_dir = os.path.dirname(root_dir)
    assert root_dir != '/', "The .project_root file was not found. Make sure it exists in your project root."
    sys.path.append(root_dir)
    return root_dir

root_dir = set_project_root()

import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.http import MediaFileUpload
import yaml



class GoogleDriveService:
    def __init__(self, auth_method):
        self.load_config()
        self._SCOPES = ['https://www.googleapis.com/auth/drive']
        self.auth_method = auth_method
    
    def load_config(self):
        with open(f"{root_dir}/config/config.yml", 'r') as file:
            cfg = yaml.safe_load(file)

        self.service_account_cred_path = cfg.get('service_account_cred_path')
        self.personal_account_cred_path = cfg.get('personal_account_cred_path')
        self.personal_account_token_path = cfg.get('personal_account_token_path')

    def build(self):
        if self.auth_method == 'service_account':
            return self.build_service_account()
        elif self.auth_method == 'personal_account':
            return self.build_personal_account()

    def build_service_account(self):
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            self.service_account_cred_path, self._SCOPES)
        return build('drive', 'v3', credentials=creds)

    def build_personal_account(self):
        creds = None
        if os.path.exists(self.personal_account_token_path):
            with open(self.personal_account_token_path, 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.personal_account_cred_path, self._SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open(self.personal_account_token_path, 'wb') as token:
                pickle.dump(creds, token)

        return build('drive', 'v3', credentials=creds)

    def folder_exists(self, name, parent_id):
        service = self.build()
        query = f"mimeType='application/vnd.google-apps.folder' and name='{name}' and '{parent_id}' in parents and trashed=false"
        response = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
        for file in response.get('files', []):
            # Assuming folder names are unique within the parent folder.
            return file.get('id')
        return None

    def list_items_owned_by_service_account(self, folder_id=None):
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.service_account_cred_path, self._SCOPES)
        service = build('drive', 'v3', credentials=creds)
        service_account_email = creds.service_account_email

        query = f"'{service_account_email}' in owners"
        if folder_id:
            query += f" and '{folder_id}' in parents"
        results = service.files().list(q=query, fields="files(id, name, mimeType, owners)").execute()
        items = results.get('files', [])
        for item in items:
            owners = [owner['emailAddress'] for owner in item.get('owners', [])]
            print(f"{'Folder' if item['mimeType'] == 'application/vnd.google-apps.folder' else 'File'}: {item['name']} (ID: {item['id']}, Owners: {owners})")
        return items


    def delete_item(self, item_id):
        service = self.build()
        item = service.files().get(fileId=item_id, fields='mimeType').execute()
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            self._delete_contents_recursive(service, item_id)
        service.files().delete(fileId=item_id).execute()
        print(f"Deleted item with ID: {item_id}")

    def _delete_contents_recursive(self, service, folder_id):
        query = f"'{folder_id}' in parents"
        results = service.files().list(q=query, fields="files(id, mimeType)").execute()
        items = results.get('files', [])

        for item in items:
            if item['mimeType'] == 'application/vnd.google-apps.folder':
                self._delete_contents_recursive(service, item['id'])
            service.files().delete(fileId=item['id']).execute()
            print(f"Deleted item: {item['id']}")

    def create_folder(self, name, parent_id):
        existing_folder_id = self.folder_exists(name, parent_id)
        if existing_folder_id:
            return existing_folder_id

        service = self.build()
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id]
        }
        folder = service.files().create(body=file_metadata, fields='id').execute()
        return folder.get('id')

    def file_exists(self, file_name, folder_id):
        service = self.build()
        query = f"name='{file_name}' and '{folder_id}' in parents and trashed=false"
        response = service.files().list(q=query, spaces='drive', fields='files(id)').execute()
        for file in response.get('files', []):
            return file.get('id')
        return None

    def upload_file(self, file_name, file_path, mime_type, folder_id, overwrite=False):
        existing_file_id = self.file_exists(file_name, folder_id)
        service = self.build()

        chunksize = 1000 * 1024 * 1024  # 1 Gigabyte
        
        if existing_file_id:
            if overwrite:
                # Overwrite the existing file

                media = MediaFileUpload(file_path, mimetype=mime_type, chunksize=chunksize, resumable=True)
                request = service.files().update(fileId=existing_file_id, media_body=media)
                response = None
                while response is None:
                    status, response = request.next_chunk()
                    if status:
                        print(f"Upload progress: {int(status.progress() * 100)}%")
                print(f"File overwritten. File ID: {response.get('id')}")
                return response.get('id')
            else:
                print(f"File '{file_name}' already exists. Skipping upload.")
                return existing_file_id
        else:
            # File does not exist, proceed with upload
            file_metadata = {'name': file_name, 'parents': [folder_id]}
            media = MediaFileUpload(file_path, mimetype=mime_type, chunksize=chunksize, resumable=True)
            request = service.files().create(body=file_metadata, media_body=media, fields='id')
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    print(f"Upload progress: {int(status.progress() * 100)}%")
            print(f"File uploaded. File ID: {response.get('id')}")
            return response.get('id')



    def upload_folder(self, local_folder_path, drive_folder_id, skip=[], overwrite=False):
        for item in os.listdir(local_folder_path):
            item_path = os.path.join(local_folder_path, item)

            # Check if item should be skipped
            if item in skip:
                print(f"Skipping: {item}")
                continue

            if os.path.isfile(item_path):
                mime_type = 'application/pdf' if item_path.endswith('.pdf') else 'application/octet-stream'
                self.upload_file(item, item_path, mime_type, drive_folder_id, overwrite=overwrite)
            elif os.path.isdir(item_path):
                new_folder_id = self.create_folder(item, drive_folder_id)
                self.upload_folder(item_path, new_folder_id, skip, overwrite)




if __name__ == "__main__":

    pass