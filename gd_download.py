# Author: Hongwei Fan(@hwfan)
# Date: Dec 25, 2019
# Last Update: Mar 23, 2020
import requests
import urllib.parse as urlparse
import sys
from downloader import save_response_content, format_size
def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None
    
def gd_download(original_url, filename, user_proxy):
    parsed_url = urlparse.urlparse(original_url)
    id = urlparse.parse_qs(parsed_url.query)['id'][0]
    URL = "https://drive.google.com/uc?export=download"
    headers={'Accept-Encoding': ''}
    session = requests.Session()
    if user_proxy is not None:
      response = session.get(URL, params = { 'id' : id }, stream = True, proxies={'http':user_proxy,'https':user_proxy}, headers=headers)
    else:
      response = session.get(URL, params = { 'id' : id }, stream = True, headers=headers)
    token = get_confirm_token(response)
    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True, proxies={'http':user_proxy,'https':user_proxy},headers=headers)
    try:
      header_size = int(response.headers['Content-Length'])
      filesize = str(format_size(header_size))
    except:
      filesize = 'Invalid'
    print('Name:%s, Size:%s' %(filename, filesize))
    save_response_content(response, filename)    
    print('Download finished.')

if __name__ == '__main__':
  print('============ GoogleDrive Direct Downloader - Debug Mode ============')
  original_url = sys.argv[1]
  filename = sys.argv[2].strip()
  user_proxy = 'socks5h://127.0.0.1:1080'
  if len(sys.argv) > 3:
    user_proxy = sys.argv[3]
  gd_download(original_url, filename, user_proxy)
