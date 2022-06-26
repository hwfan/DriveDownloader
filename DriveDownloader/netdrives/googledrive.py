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
from rich.console import Console

googleauthdata = \
'''
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

info = \
'''
+-------------------------------------------------------------------+
|Warning: DriveDownloader is using the backup downloader due to the |
|forbiddance or manual setting. If this is the first time you meet  |
|the notice, please follow the instructions to login your Google    |
|Account. This operation only needs to be done once.                |
+-------------------------------------------------------------------+
'''

console = Console(width=71)
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

    def connect(self, url, custom_filename='', force_backup=False, proc_id=-1):
      replaced_url, id_str = self.generate_url(url)
      if force_backup:
        self.backup_connect(url, custom_filename, id_str, proc_id=proc_id)
        return
      try:
        self.params["id"] = id_str
        self.params["confirm"] = "t"
        DriveSession.connect(self, replaced_url, custom_filename=custom_filename)
      except:
        self.backup_connect(url, custom_filename, id_str, proc_id=proc_id)
    
    def backup_connect(self, url, custom_filename, id_str, proc_id=-1):
      if proc_id == -1:
        console.print(info)
      settings_file_path = os.path.join(os.path.dirname(__file__), 'settings.yaml')
      if not os.path.exists(settings_file_path):
        with open(settings_file_path, "w") as f:
          f.write(googleauthdata)
      self.gauth = GoogleAuth(settings_file=settings_file_path)
      self.gauth.CommandLineAuth()
      self.gid_str = id_str
      drive = GoogleDrive(self.gauth)
      file = drive.CreateFile({"id": id_str})
      self.filename = file['title'] if len(custom_filename) == 0 else custom_filename
      self.filesize = float(file['fileSize'])
      self.response = self.gauth.service.files().get_media(fileId=id_str)