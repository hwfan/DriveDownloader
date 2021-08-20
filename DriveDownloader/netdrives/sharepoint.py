#############################################
#  Author: Hongwei Fan                      #
#  E-mail: hwnorm@outlook.com               #
#  Homepage: https://github.com/hwfan       #
#############################################
import urllib.parse as urlparse
from DriveDownloader.netdrives.basedrive import DriveSession

class SharePointSession(DriveSession):
    def __init__(self, proxy, chunk_size=32768):
        DriveSession.__init__(self, proxy, chunk_size)

    def generate_url(self, url):
        '''
        Solution provided by:
        https://www.qian.blue/archives/OneDrive-straight.html
        '''
        parsed_url = urlparse.urlparse(url)
        path = parsed_url.path
        netloc = parsed_url.netloc
        splitted_path = path.split('/')
        personal_attr, domain, sharelink = splitted_path[3:6]
        resultUrl = f"https://{netloc}/{personal_attr}/{domain}/_layouts/52/download.aspx?share={sharelink}"
        return resultUrl

    def connect(self, url, custom_filename=''):
        onedrive_url = self.generate_url(url)
        DriveSession.connect(self, onedrive_url, download=True, custom_filename=custom_filename)