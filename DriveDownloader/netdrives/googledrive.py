#############################################
#  Author: Hongwei Fan                      #
#  E-mail: hwnorm@outlook.com               #
#  Homepage: https://github.com/hwfan       #
#############################################
import urllib.parse as urlparse
from DriveDownloader.netdrives.basedrive import DriveSession
from DriveDownloader.pydrive2.auth import GoogleAuth
from DriveDownloader.pydrive2.drive import GoogleDrive

import os
import sys

googleauthdata = '''
client_config_backend: settings
client_config:
  client_id: 367116221053-7n0vf5akeru7on6o2fjinrecpdoe99eg.apps.googleusercontent.com
  client_secret: 1qsNodXNaWq1mQuBjUjmvhoO

save_credentials: True
save_credentials_backend: file

get_refresh_token: True

oauth_scope:
  - https://www.googleapis.com/auth/drive
'''

class GoogleDriveSession(DriveSession):
    def __init__(self, *args, **kwargs):
        DriveSession.__init__(self, *args, **kwargs)
    
    def generate_url(self, url):
        '''
        Solution provided by:
        https://stackoverflow.com/questions/25010369/wget-curl-large-file-from-google-drive
        '''
        parsed_url = urlparse.urlparse(url)
        parsed_qs = urlparse.parse_qs(parsed_url.query)
        if 'id' in parsed_qs:
          id_str = parsed_qs['id'][0]
        else:
          id_str = parsed_url.path.split('/')[3]
        replaced_url = "https://drive.google.com/u/0/uc?export=download"
        return replaced_url, id_str

    def connect(self, url, custom_filename=''):
      replaced_url, id_str = self.generate_url(url)
      try:
        self.params["id"] = id_str
        self.params["confirm"] = "t"
        DriveSession.connect(self, replaced_url, custom_filename=custom_filename)
      except:
        info = '''+-------------------------------------------------------------------------------------------+
|Warning: The default request is forbidden by GoogleDrive due to the frequent downloading,  |
|and DriveDownloader is now using the backup downloader. If this is the first time you meet |
|the problem, please follow the instructions to login your Google Account. Once this action |
|is performed, the downloading procedure will automatically start for all the time.         |
+-------------------------------------------------------------------------------------------+'''
        sys.stdout.write(info+'\n')
        settings_file_path = os.path.join(os.path.dirname(__file__), 'settings.yaml')
        if not os.path.exists(settings_file_path):
          with open(settings_file_path, "w") as f:
            f.write(googleauthdata)
        gauth = GoogleAuth(settings_file=settings_file_path)
        gauth.CommandLineAuth()
        drive = GoogleDrive(gauth)
        file = drive.CreateFile({"id": id_str})
        self.filename = file['title'] if len(custom_filename) == 0 else custom_filename
        self.filesize = float(file['fileSize'])
        self.response = gauth.service.files().get_media(fileId=id_str)