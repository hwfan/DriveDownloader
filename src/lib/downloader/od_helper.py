# Author: Hongwei Fan(@hwfan)
# Date: Dec 25, 2019
# Last Update: Sep 13, 2020
import requests
import urllib.parse as urlparse
import sys
from lib.utils.content_processor import *

def od_download(url, custom_filename, user_proxy):
    headers={'Accept-Encoding': ''}
    session = requests.Session()
    
    parsed_url = urlparse.urlparse(url)
    replaced_parsed = parsed_url._replace(netloc='1drv.ws')
    replaced_url = urlparse.urlunparse(replaced_parsed)
    if user_proxy is not None:
      response = session.get(replaced_url, stream = True, proxies={"http":user_proxy,"https":user_proxy}, headers=headers)
    else:
      response = session.get(replaced_url, stream = True, headers=headers)

    filename_parsed, filesize = parse_response_header(response)
    filename = filename_parsed if len(custom_filename) == 0 else custom_filename
    save_response_content(response, filename, filesize)
    
if __name__ == '__main__':
  print('============ OneDrive Direct Downloader - Debug Mode ============')
  url = sys.argv[1]
  filename = sys.argv[2].strip()
  user_proxy = 'socks5h://127.0.0.1:1080'
  if len(sys.argv) > 3:
    user_proxy = sys.argv[3]
  od_download(url, filename, user_proxy)