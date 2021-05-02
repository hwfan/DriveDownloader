#############################################
#  Author: Hongwei Fan                      #
#  E-mail: hwnorm@outlook.com               #
#  Homepage: https://github.com/hwfan       #
#############################################
import requests
import sys
import re
from tqdm import tqdm
from DriveDownloader.utils.misc import *
from fake_useragent import UserAgent

class DriveSession:
  def __init__(self, proxy=None, chunk_size=32768):
    self.session = requests.Session()
    self.ua = UserAgent(verify_ssl=False)
    if proxy is None:
        self.proxies = None
    else:
        self.proxies = { "http": proxy, "https": proxy, }
    self.params = dict()
    self.chunk_size = chunk_size
    self.headers = { 'Accept-Encoding': '', 'User-Agent': self.ua.random, }
  
  def generate_url(self, url):
    raise NotImplementedError

  def parse_response_header(self, response):
    try:
        pattern = re.compile(r'filename=\"(.*?)\"')
        filename = pattern.findall(response.headers['content-disposition'])[0]
    except:
        filename = 'noname.out'

    try:
        header_size = int(response.headers['Content-Length'])
    except:
        header_size = None

    return filename, header_size

  def save_response_content(self, response, filename, filesize):
    filesize_str = str(format_size(filesize)) if filesize is not None else 'Invalid'
    sys.stdout.write('Name: {:s}, Size: {:s}\n'.format(filename, filesize_str))
    progress_bar = tqdm(total=filesize, ncols=47, unit='B', unit_scale=True, unit_divisor=1024)

    with open(filename, "wb") as f:
        for chunk in response.iter_content(self.chunk_size):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                chunk_num = len(chunk)
                progress_bar.update(chunk_num)
    progress_bar.close()
    
    sys.stdout.write('Download finished.\n')

  def connect(self, url, download=False, custom_filename=''):
    response = self.session.get(url, params=self.params, proxies=self.proxies, stream=True, headers=self.headers)
    if download:
        filename_parsed, filesize = self.parse_response_header(response)
        filename = filename_parsed if len(custom_filename) == 0 else custom_filename
        self.save_response_content(response, filename, filesize)
    return response