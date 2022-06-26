#############################################
#  Author: Hongwei Fan                      #
#  E-mail: hwnorm@outlook.com               #
#  Homepage: https://github.com/hwfan       #
#############################################
import urllib.parse as urlparse
from DriveDownloader.netdrives.basedrive import DriveSession

class DropBoxSession(DriveSession):
    def __init__(self, *args, **kwargs):
        DriveSession.__init__(self, *args, **kwargs)

    def generate_url(self, url):
        '''
        Solution provided by:
        https://sunpma.com/564.html
        '''
        parsed_url = urlparse.urlparse(url)
        netloc = parsed_url.netloc.replace('www', 'dl-web')
        query = ''
        parsed_url = parsed_url._replace(netloc=netloc, query=query)
        resultUrl = urlparse.urlunparse(parsed_url)
        return resultUrl

    def connect(self, url, custom_filename='', proc_id=-1, force_backup=False):
        generated_url = self.generate_url(url)
        DriveSession.connect(self, generated_url, custom_filename=custom_filename)