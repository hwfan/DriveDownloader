#############################################
#  Author: Hongwei Fan                      #
#  E-mail: hwnorm@outlook.com               #
#  Homepage: https://github.com/hwfan       #
#############################################
import urllib.parse as urlparse
import os
from DriveDownloader.netdrives.basedrive import DriveSession

class DirectLink(DriveSession):
    def __init__(self, *args, **kwargs):
        DriveSession.__init__(self, *args, **kwargs)

    def parse_response_header(self):
        filename = os.path.basename(self.response.url)
        try:
            header_size = int(self.response.headers['Content-Length'])
        except:
            header_size = None

        return filename, header_size

    def generate_url(self, url):
        return url

    def connect(self, url, custom_filename='', proc_id=-1, force_backup=False):
        generated_url = self.generate_url(url)
        DriveSession.connect(self, generated_url, custom_filename=custom_filename)