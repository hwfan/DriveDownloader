# Author: Hongwei Fan(@hwfan)
# Date: Dec 25, 2019
# Last Update: Mar 23, 2020
import time
import sys
import re
from tqdm import tqdm

def format_size(num_size):
    try:
        num_size = float(num_size)
        KB = num_size / 1024
    except:
        return "Error"
    if KB >= 1024:
        M = KB / 1024
        if M >= 1024:
            G = M / 1024
            return '%.3f GB' % G
        else:
            return '%.3f MB' % M
    else:
        return '%.3f KB' % KB 

def save_response_content(response, filename, filesize):
    filesize_str = str(format_size(filesize)) if filesize is not None else 'Invalid'
    print('Name:%s, Size:%s' %(filename, filesize_str))
    progress_bar = tqdm(total=filesize, unit='B', unit_scale=True, unit_divisor=1024)
    
    CHUNK_SIZE = 32768
    total = 0
    start_time = time.time()
    with open(filename, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                interval = time.time()-start_time
                chunk_num = len(chunk)
                total += chunk_num
                speed = total/interval
                progress_bar.update(chunk_num)
                # sys.stdout.write('Downloaded: '+format_size(total).ljust(11, ' ')+'\tSpeed: '+(format_size(speed)+'/s').ljust(13, ' '))
                # sys.stdout.flush()
                # sys.stdout.write('\r')
    # sys.stdout.write('\n')
    progress_bar.close()
    print('Download finished.')

def parse_response_header(response):
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

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None