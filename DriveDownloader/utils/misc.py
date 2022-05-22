#############################################
#  Author: Hongwei Fan                      #
#  E-mail: hwnorm@outlook.com               #
#  Homepage: https://github.com/hwfan       #
#############################################
from urllib.parse import urlparse

def format_size(value):
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = 1024.0
    for i in range(len(units)):
        if (value / size) < 1:
            return "%.2f %s" % (value, units[i])
        value = value / size
    return value

def judge_session(url):
    if '1drv.ms' in url or '1drv.ws' in url:
        return 'OneDrive'
    elif 'drive.google.com' in url:
        return 'GoogleDrive'
    elif 'sharepoint' in url:
        return 'SharePoint'
    elif 'dropbox' in url:
        return 'DropBox'
    else:
        return 'DirectLink'

def judge_scheme(url):
    return urlparse(url).scheme