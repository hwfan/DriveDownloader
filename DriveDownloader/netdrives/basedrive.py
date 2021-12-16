#############################################
#  Author: Hongwei Fan                      #
#  E-mail: hwnorm@outlook.com               #
#  Homepage: https://github.com/hwfan       #
#############################################
import requests
import sys
import re
import os
from tqdm import tqdm
from DriveDownloader.utils.misc import *

class DriveSession:
  def __init__(self, proxy=None, chunk_size=32768):
    self.session = requests.Session()
    if proxy is None:
        self.proxies = None
    else:
        self.proxies = { "http": proxy, "https": proxy, }
    self.params = dict()
    self.chunk_size = chunk_size
    self.headers = { 'Accept-Encoding': '', }
    self.filename = ''
    self.filesize = None
    self.response = None
    self.file_handler = None
    
  def generate_url(self, url):
    raise NotImplementedError
  
  def set_range(self, start, end):
    self.headers['Range'] = 'bytes={:s}-{:s}'.format(start, end)

  def parse_response_header(self):
    try:
        pattern = re.compile(r'filename=\"(.*?)\"')
        filename = pattern.findall(self.response.headers['content-disposition'])[0]
    except:
        filename = 'noname.out'

    try:
        header_size = int(self.response.headers['Content-Length'])
    except:
        header_size = None

    return filename, header_size

  def save_response_content(self, start=None, proc_id=-1):
    dirname = os.path.dirname(self.filename)
    if len(dirname) > 0:
        os.makedirs(dirname, exist_ok=True)
    
    if proc_id == -1:
      self.file_handler = open(self.filename, "wb")
      progress_bar = tqdm(total=self.filesize, ncols=47, unit='B', unit_scale=True, unit_divisor=1024)
      for chunk in self.response.iter_content(self.chunk_size):
          if chunk: # filter out keep-alive new chunks
              self.file_handler.write(chunk)
              chunk_num = len(chunk)
              progress_bar.update(chunk_num)
      progress_bar.close()
    else:
      name, ext = os.path.splitext(self.filename)
      name = name + '_{}'.format(proc_id)
      sub_filename = name + ext
      sub_dirname = os.path.dirname(sub_filename)
      sub_basename = os.path.basename(sub_filename)
      sub_tmp_dirname = os.path.join(sub_dirname, 'tmp')
      os.makedirs(sub_tmp_dirname, exist_ok=True)
      sub_filename = os.path.join(sub_tmp_dirname, sub_basename)
      self.file_handler = open(sub_filename, "wb")
      progress_bar = tqdm(total=self.filesize, ncols=47, unit='B', unit_scale=True, unit_divisor=1024, desc='proc {}'.format(proc_id))
      for chunk in self.response.iter_content(self.chunk_size):
          if chunk: # filter out keep-alive new chunks
              self.file_handler.write(chunk)
              chunk_num = len(chunk)
              progress_bar.update(chunk_num)
      progress_bar.close()

  def connect(self, url, custom_filename=''):
    self.response = self.session.get(url, params=self.params, proxies=self.proxies, stream=True, headers=self.headers)
    filename_parsed, self.filesize = self.parse_response_header()
    self.filename = filename_parsed if len(custom_filename) == 0 else custom_filename

  def show_info(self):
    filesize_str = str(format_size(self.filesize)) if self.filesize is not None else 'Invalid'
    sys.stdout.write('Name: {:s}, Size: {:s}\n'.format(self.filename, filesize_str))