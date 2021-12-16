#############################################
#  Author: Hongwei Fan                      #
#  E-mail: hwnorm@outlook.com               #
#  Homepage: https://github.com/hwfan       #
#############################################
from .googledrive import GoogleDriveSession
from .onedrive import OneDriveSession
from .sharepoint import SharePointSession
from .dropbox import DropBoxSession
from .directlink import DirectLink

__factory__ = {"GoogleDrive": GoogleDriveSession,
               "OneDrive": OneDriveSession,
               "SharePoint": SharePointSession,
               "DropBox": DropBoxSession,
               "DirectLink": DirectLink,
            }

def get_session(name):
    return __factory__[name]
