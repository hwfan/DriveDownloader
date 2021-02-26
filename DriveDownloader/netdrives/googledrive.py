#############################################
#  Author: Hongwei Fan                      #
#  E-mail: hwnorm@outlook.com               #
#  Homepage: https://github.com/hwfan       #
#############################################
import urllib.parse as urlparse
from DriveDownloader.netdrives.basedrive import DriveSession

class GoogleDriveSession(DriveSession):
    def __init__(self, proxy, chunk_size=32768):
        DriveSession.__init__(self, proxy, chunk_size)
    
    def generate_url(self, url):
        parsed_url = urlparse.urlparse(url)
        parsed_qs = urlparse.parse_qs(parsed_url.query)
        if 'id' in parsed_qs:
          id_str = parsed_qs['id'][0]
        else:
          id_str = parsed_url.path.split('/')[3]
        replaced_url = "https://drive.google.com/uc?export=download"
        return replaced_url, id_str

    def get_confirm_token(self, response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None

    def connect(self, url, custom_filename=''):
        replaced_url, id_str = self.generate_url(url)
        self.params["id"] = id_str
        response = DriveSession.connect(self, replaced_url, download=False, custom_filename=custom_filename)
        token = self.get_confirm_token(response)
        if token:
          self.params["confirm"] = token
        DriveSession.connect(self, replaced_url, download=True, custom_filename=custom_filename)