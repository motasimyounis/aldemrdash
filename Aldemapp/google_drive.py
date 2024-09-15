from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload



def upload_to_google_drive(file_path, file_name):
    SCOPES = ['https://www.googleapis.com/auth/drive.file']

    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {'name': file_name, 'mimeType': 'application/pdf'}
    media = MediaFileUpload(file_path, mimetype='application/pdf')

    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')




def set_file_permissions(file_id):
    SCOPES = ['https://www.googleapis.com/auth/drive']

    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('drive', 'v3', credentials=creds)

    permission = {
        'role': 'reader',
        'type': 'anyone',
        'allowFileDiscovery': False,
        'withLink': True
    }

    service.permissions().create(fileId=file_id, body=permission).execute()

    # Prevent downloading, printing, and copying
    service.files().update(fileId=file_id, body={
        'copyRequiresWriterPermission': True,
        'writersCanShare': False,
        'permissions': [
            {
                'type': 'anyone',
                'role': 'reader',
                'allowFileDiscovery': False,
                'viewersCanCopyContent': False
            }
        ]
    }).execute()
