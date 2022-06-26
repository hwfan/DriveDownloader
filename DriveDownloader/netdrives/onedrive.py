#############################################
#  Author: Hongwei Fan                      #
#  E-mail: hwnorm@outlook.com               #
#  Homepage: https://github.com/hwfan       #
#############################################
import base64
from DriveDownloader.netdrives.basedrive import DriveSession

class OneDriveSession(DriveSession):
    def __init__(self, *args, **kwargs):
        DriveSession.__init__(self, *args, **kwargs)

    def generate_url(self, url):
        '''
        Solution provided by:
        https://towardsdatascience.com/how-to-get-onedrive-direct-download-link-ecb52a62fee4
        '''
        data_bytes64 = base64.b64encode(bytes(url, 'utf-8'))
        data_bytes64_String = data_bytes64.decode('utf-8').replace('/','_').replace('+','-').rstrip("=")
        resultUrl = f"https://api.onedrive.com/v1.0/shares/u!{data_bytes64_String}/root/content"
        return resultUrl

    def connect(self, url, custom_filename='', proc_id=-1, force_backup=False):
        generated_url = self.generate_url(url)
        DriveSession.connect(self, generated_url, custom_filename=custom_filename)