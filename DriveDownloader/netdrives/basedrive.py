#############################################
#  Author: Hongwei Fan                      #
#  E-mail: hwnorm@outlook.com               #
#  Homepage: https://github.com/hwfan       #
#############################################
import requests
import requests_random_user_agent
import sys
import re
import os
from tqdm import tqdm
from DriveDownloader.utils.misc import *
from threading import Event
import signal
from rich.console import Console
from googleapiclient.http import _retry_request, DEFAULT_CHUNK_SIZE
import time
import random

console = Console(width=71)
done_event = Event()
def handle_sigint(signum, frame):
    console.print("\n[yellow]Interrupted. Will shutdown after the latest chunk is downloaded.\n")
    done_event.set()
signal.signal(signal.SIGINT, handle_sigint)

class DriveSession:
  def __init__(self, proxy=None, chunk_size=32768):
    self.session = requests.Session()
    self.session.headers['Accept-Encoding'] = ''
    if proxy is None:
        self.proxies = None
    else:
        self.proxies = { "http": proxy, "https": proxy, }
    self.params = dict()
    self.chunk_size = chunk_size
    self.filename = ''
    self.filesize = None
    self.response = None
    self.file_handler = None
    self.base_url = None

  def generate_url(self, url):
    raise NotImplementedError
  
  def set_range(self, start, end):
    self.session.headers['Range'] = 'bytes={:s}-{:s}'.format(str(start), str(end))
    
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

  def save_response_content(self, start=None, end=None, proc_id=-1, progress_bar=None):
    dirname = os.path.dirname(self.filename)
    if len(dirname) > 0:
        os.makedirs(dirname, exist_ok=True)
    interrupted = False

    if proc_id >= 0:
      name, ext = os.path.splitext(self.filename)
      name = name + '_{}'.format(proc_id)
      sub_filename = name + ext
      sub_dirname = os.path.dirname(sub_filename)
      sub_basename = os.path.basename(sub_filename)
      sub_tmp_dirname = os.path.join(sub_dirname, 'tmp')
      os.makedirs(sub_tmp_dirname, exist_ok=True)
      sub_filename = os.path.join(sub_tmp_dirname, sub_basename)
      used_filename = sub_filename
    else:
      proc_id = 0
      used_filename = self.filename
      start = 0
      end = self.filesize-1

    ori_filesize = os.path.getsize(used_filename) if os.path.exists(used_filename) else 0
    self.file_handler = open(used_filename, 'ab' if ori_filesize > 0 else 'wb' )
    progress_bar.update(proc_id, total=end+1-start)
    progress_bar.start_task(proc_id)
    progress_bar.update(proc_id, advance=ori_filesize)

    if 'googleapiclient' in str(type(self.response)):
      self.chunk_size = 1 * 1024 * 1024
      _headers = {}
      for k, v in self.response.headers.items():
        if not k.lower() in ("accept", "accept-encoding", "user-agent"):
            _headers[k] = v
      cur_state = start + ori_filesize
      while cur_state < end + 1:
        headers = _headers.copy()
        remained = end + 1 - cur_state
        chunk_size = self.chunk_size if remained >= self.chunk_size else remained
        headers["range"] = "bytes=%d-%d" % (
            cur_state,
            cur_state + chunk_size - 1,
        )
        http = self.response.http
        resp, content = _retry_request(
            http,
            0,
            "media download",
            time.sleep,
            random.random,
            self.response.uri,
            "GET",
            headers=headers,
        )
        self.file_handler.write(content)
        progress_bar.update(proc_id, advance=len(content))
        cur_state += len(content)
        if done_event.is_set():
            interrupted = True
            return interrupted
    else:
      if ori_filesize > 0:
        self.set_range(start + ori_filesize, end)
        self.response = self.session.get(self.base_url, params=self.params, proxies=self.proxies, stream=True)
      else:
        self.set_range(start, end)
      cur_state = start + ori_filesize
      for chunk in self.response.iter_content(self.chunk_size):
        if cur_state >= end + 1:
          break
        self.file_handler.write(chunk)
        chunk_num = len(chunk)
        progress_bar.update(proc_id, advance=chunk_num)
        cur_state += chunk_num
        if done_event.is_set():
          interrupted = True
          return interrupted
          
  def connect(self, url, custom_filename=''):
    self.base_url = url
    self.response = self.session.get(url, params=self.params, proxies=self.proxies, stream=True)
    if self.response.status_code // 100 >= 4:
      raise RuntimeError("Bad status code {}. Please check your connection.".format(self.response.status_code))
    filename_parsed, self.filesize = self.parse_response_header()
    self.filename = filename_parsed if len(custom_filename) == 0 else custom_filename
    
  def show_info(self, progress_bar, list_suffix):
    filesize_str = str(format_size(self.filesize)) if self.filesize is not None else 'Invalid'
    progress_bar.console.print('{:s}Name: {:s}, Size: {:s}'.format(list_suffix+' ' if list_suffix else '', self.filename, filesize_str))