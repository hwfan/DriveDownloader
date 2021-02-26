#############################################
#  Author: Hongwei Fan                      #
#  E-mail: hwnorm@outlook.com               #
#  Homepage: https://github.com/hwfan       #
#############################################
import urllib.parse as urlparse
from DriveDownloader.netdrives.basedrive import DriveSession

class OneDriveSession(DriveSession):
    def __init__(self, proxy, chunk_size=32768):
        DriveSession.__init__(self, proxy, chunk_size)
    
    def generate_url(self, url):
        parsed_url = urlparse.urlparse(url)
        replaced_parsed = parsed_url._replace(netloc='1drv.ws')
        replaced_url = urlparse.urlunparse(replaced_parsed)
        return replaced_url

    def connect(self, url, custom_filename=''):
        onedrive_url = self.generate_url(url)
        DriveSession.connect(self, onedrive_url, download=True, custom_filename=custom_filename)