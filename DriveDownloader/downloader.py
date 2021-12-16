#############################################
#  Author: Hongwei Fan                      #
#  E-mail: hwnorm@outlook.com               #
#  Homepage: https://github.com/hwfan       #
#############################################
from DriveDownloader.netdrives import get_session
from DriveDownloader.utils import judge_session, MultiThreadDownloader
import argparse
import os
import sys

def parse_args():
    parser = argparse.ArgumentParser(description='Drive Downloader Args')
    parser.add_argument('url', help='URL you want to download from.', default='', type=str)
    parser.add_argument('--filename', '-o', help='Target file name.', default='', type=str)
    parser.add_argument('--proxy', '-p', help='Proxy address when needed.', default='', type=str)
    parser.add_argument('--list', '-l', help='Choose whether the input is a filelist.', action='store_true')
    parser.add_argument('--list-disp', help='The display frequency of list downloading.', type=int, default=1)
    parser.add_argument('--thread-number', '-n', help='thread number of multithread.', type=int, default=1)
    args = parser.parse_args()
    return args

def download_single_file(url, proxy="", filename="", thread_number=1):
    used_proxy = proxy if len(proxy) > 0 and proxy != 'None' else None
    session_name = judge_session(url)
    session_func = get_session(session_name)
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
        if (line_idx + 1) % args.list_disp == 0:
            sys.stdout.write("Filelist downloaded {:d} / {:d}\n".format(line_idx+1, len(lines)))

def simple_cli():
    assert len(sys.argv) > 1, "Please input your URL or filelist path!"
    sys.stdout.write('============ Drive Downloader ============\n')
    args = parse_args()
    if not args.list:
        download_single_file(args.url, args.proxy, args.filename, args.thread_number)
    else:
        sys.stdout.write('Downloading filelist: {:s}\n'.format(os.path.basename(args.url)))
        download_filelist(args)
    sys.stdout.write('Download finished.\n')

if __name__ == '__main__':
    simple_cli()
