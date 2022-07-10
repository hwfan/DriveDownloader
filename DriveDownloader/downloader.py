#############################################
#  Author: Hongwei Fan                      #
#  E-mail: hwnorm@outlook.com               #
#  Homepage: https://github.com/hwfan       #
#############################################
from DriveDownloader.netdrives import get_session
from DriveDownloader.utils import judge_session, MultiThreadDownloader, judge_scheme
import argparse
import os
import sys
__version__ = "1.5.0"
url_scheme_env_key_map = {
        "http": "http_proxy",
        "https": "https_proxy",
}

def parse_args():
    parser = argparse.ArgumentParser(description='Drive Downloader Args')
    parser.add_argument('url', help='URL you want to download from.', default='', type=str)
    parser.add_argument('--filename', '-o', help='Target file name.', default='', type=str)
    parser.add_argument('--thread-number', '-n', help='thread number of multithread.', type=int, default=1)
    parser.add_argument('--version', '-v', action='version', version=__version__, help='Version.')
    args = parser.parse_args()
    return args

def get_env(key):
    value = os.environ.get(key)
    if not value or len(value) == 0:
        return None
    return value

def download_single_file(url, filename="", thread_number=1):
    scheme = judge_scheme(url)
    if scheme not in url_scheme_env_key_map.keys():
        raise NotImplementedError(f"Unsupported scheme {scheme}")
    env_key = url_scheme_env_key_map[scheme]
    used_proxy = get_env(env_key)

    session_name = judge_session(url)
    session_func = get_session(session_name)
    if session_name == 'GoogleDrive' and thread_number > 1:
        sys.stdout.write('Warning: Google Drive URL detected. Only one thread will be created.\n')
        thread_number = 1
    download_session = session_func(used_proxy)
    download_session.connect(url, filename)
    final_filename = download_session.filename
    download_session.show_info()
    if thread_number > 1:
        download_session = MultiThreadDownloader(session_func, used_proxy, download_session.filesize, thread_number)
        download_session.get(url, final_filename)
        download_session.concatenate(final_filename)
    else:
        download_session.save_response_content()

def download_filelist(args):
    lines = [line for line in open(args.url, 'r')]
    for line_idx, line in enumerate(lines):
        splitted_line = line.strip().split(" ")
        download_single_file(*splitted_line, args.thread_number)
        sys.stdout.write("Filelist downloaded {:d} / {:d}\n".format(line_idx+1, len(lines)))

def simple_cli():
    sys.stdout.write('============ Drive Downloader ============\n')
    args = parse_args()
    assert len(args.url) > 0, "Please input your URL or filelist path!"
    if os.path.exists(args.url):
        sys.stdout.write('Downloading filelist: {:s}\n'.format(os.path.basename(args.url)))
        download_filelist(args)
    else:
        download_single_file(args.url, args.filename, args.thread_number)
        
    sys.stdout.write('Download finished.\n')

if __name__ == '__main__':
    simple_cli()
