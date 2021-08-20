#############################################
#  Author: Hongwei Fan                      #
#  E-mail: hwnorm@outlook.com               #
#  Homepage: https://github.com/hwfan       #
#############################################
import urllib.parse as urlparse
from DriveDownloader.netdrives.basedrive import DriveSession

class DropBoxSession(DriveSession):
    def __init__(self, proxy, chunk_size=32768):
        DriveSession.__init__(self, proxy, chunk_size)

    def generate_url(self, url):
        '''
        Solution provided by:
        https://www.qian.blue/archives/OneDrive-straight.html
        '''
        parsed_url = urlparse.urlparse(url)
        netloc = parsed_url.netloc.replace('www', 'dl-web')
        query = ''
        parsed_url = parsed_url._replace(netloc=netloc, query=query)
        resultUrl = urlparse.urlunparse(parsed_url)
        return resultUrl

    def connect(self, url, custom_filename=''):
        onedrive_url = self.generate_url(url)
        DriveSession.connect(self, onedrive_url, download=True, custom_filename=custom_filename)