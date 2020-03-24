# Author: Hongwei Fan(@hwfan)
# Date: Dec 25, 2019
# Last Update: Mar 23, 2020
import requests
import urllib.parse as urlparse
import sys
import os
from downloader import save_response_content,format_size
def od_download(url, filename, user_proxy):
    headers={'Accept-Encoding': ''}
    if user_proxy is not None:
      proxy = {"http":user_proxy,"https":user_proxy}
    else:
      proxy = None
    session = requests.Session()
    
    parsed_url = urlparse.urlparse(url)
    target = '1drv.ws'
    replaced_parsed = parsed_url._replace(netloc=target)
    replaced_url = urlparse.urlunparse(replaced_parsed)
    if proxy is not None:
      response = session.get(replaced_url, stream = True, proxies=proxy, headers=headers)
    else:
      response = session.get(replaced_url, stream = True, headers=headers)
    try:
      header_size = int(response.headers['content-length'])
      # print(response.headers)
      filesize = str(format_size(header_size))
    except:
      filesize = 'Invalid'
    print('Name:%s, Size:%s' %(filename, filesize))
    
    save_response_content(response, filename)    
    print('Download finished.')
if __name__ == '__main__':
  print('============ OneDrive Direct Downloader - Debug Mode ============')
  url = sys.argv[1]
  filename = sys.argv[2].strip()
  user_proxy = 'socks5h://127.0.0.1:1080'
  if len(sys.argv) > 3:
    user_proxy = sys.argv[3]
  od_download(url, filename, user_proxy)