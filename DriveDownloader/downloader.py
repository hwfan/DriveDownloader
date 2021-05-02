#############################################
#  Author: Hongwei Fan                      #
#  E-mail: hwnorm@outlook.com               #
#  Homepage: https://github.com/hwfan       #
#############################################
from DriveDownloader.netdrives.googledrive import GoogleDriveSession
from DriveDownloader.netdrives.onedrive import OneDriveSession
import argparse
import os
import sys

def parse_args():
    parser = argparse.ArgumentParser(description='Drive Downloader Args')
    parser.add_argument('url', help='URL you want to download from.', default='', type=str)
    parser.add_argument('--filename', help='Target file name.', default='', type=str)
    parser.add_argument('--proxy', help='Proxy address when needed.', default='', type=str)
    args = parser.parse_args()
    return args

def simple_cli():

    sys.stdout.write('============ Drive Downloader V1.2 ============\n')

    if len(sys.argv) > 1:
        # non-interactive mode
        args = parse_args()
        url = args.url
        assert len(url) > 0, "Invalid URL!"
        filename = args.filename
        proxy = args.proxy
    else:
        # interactive mode
        url = input("URL: ").strip()
        assert len(url) > 0, "Invalid URL!"
        filename = input("Filename: ").strip()
        proxy = input("Proxy: ").strip()

    final_filename = '' if len(filename) == 0 else filename
    dirname = os.path.dirname(final_filename)
    if len(dirname) > 0:
        os.makedirs(dirname, exist_ok=True)
    final_proxy = proxy if len(proxy) > 0 else None

    if '1drv.ms' in url or '1drv.ws' in url:
        download_session = OneDriveSession(final_proxy)
    elif 'drive.google.com' in url:
        download_session = GoogleDriveSession(final_proxy)
    else:
        raise NotImplementedError("The drive type is not supported!")
    
    download_session.connect(url, final_filename)
    
if __name__ == '__main__':
    simple_cli()
