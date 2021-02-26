#############################################
#  Author: Hongwei Fan                      #
#  E-mail: hwnorm@outlook.com               #
#  Homepage: https://github.com/hwfan       #
#############################################
from DriveDownloader.netdrives.googledrive import GoogleDriveSession
from DriveDownloader.netdrives.onedrive import OneDriveSession
import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser(description='Drive Downloader Args')
    parser.add_argument('url', help='URL you want to download from.', default='', type=str)
    parser.add_argument('--filename', help='Target file name.', default='', type=str)
    parser.add_argument('--proxy', help='Proxy address when needed.', default='', type=str)
    args = parser.parse_args()
    return args

def simple_cli():
    args = parse_args()
    assert len(args.url) > 0

    print('============ Drive Downloader V1.2 ============')
    final_proxy = args.proxy.strip() if len(args.proxy) > 0 else None

    if '1drv.ms' in args.url or '1drv.ws' in args.url:
        download_session = OneDriveSession(final_proxy)
    elif 'drive.google.com' in args.url:
        download_session = GoogleDriveSession(final_proxy)
    else:
        raise NotImplementedError("The drive type is not supported!")
    
    download_session.connect(args.url.strip(), args.filename.strip())
    
if __name__ == '__main__':
    simple_cli()
