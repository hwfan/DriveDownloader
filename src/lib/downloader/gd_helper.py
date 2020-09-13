# Author: Hongwei Fan(@hwfan)
# Date: Dec 25, 2019
# Last Update: Sep 13, 2020
import requests
import urllib.parse as urlparse
import sys
from lib.utils.content_processor import *
from fake_useragent import UserAgent

def gd_download(url, custom_filename, user_proxy):
    ua = UserAgent(verify_ssl=False)

    parsed_url = urlparse.urlparse(url)
    parsed_qs = urlparse.parse_qs(parsed_url.query)
    if 'id' in parsed_qs:
      id_str = parsed_qs['id'][0]
    else:
      id_str = parsed_url.path.split('/')[3]
    URL = "https://drive.google.com/uc?export=download"
    headers={'Accept-Encoding': '', 'User-Agent':ua.random}
    session = requests.Session()
    if user_proxy is not None:
      response = session.get(URL, params = { 'id' : id_str }, stream = True, proxies={'https':user_proxy}, headers=headers)
    else:
      response = session.get(URL, params = { 'id' : id_str }, stream = True, headers=headers)
    token = get_confirm_token(response)
    print('confirm token: %s' % token)
    if token:
        params = { 'id' : id_str, 'confirm' : token }
        if user_proxy is not None:
          response = session.get(URL, params = params, proxies={'https':user_proxy}, stream = True, headers=headers)
        else:
          response = session.get(URL, params = params, stream = True, headers=headers)
    
    filename_parsed, filesize = parse_response_header(response)
    filename = filename_parsed if len(custom_filename) == 0 else custom_filename
    save_response_content(response, filename, filesize)    
    

if __name__ == '__main__':
  print('============ GoogleDrive Direct Downloader - Debug Mode ============')
  original_url = sys.argv[1]
  filename = sys.argv[2].strip()
  user_proxy = 'socks5h://127.0.0.1:1080'
  if len(sys.argv) > 3:
    user_proxy = sys.argv[3]
  gd_download(original_url, filename, user_proxy)
