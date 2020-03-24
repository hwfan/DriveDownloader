# Author: Hongwei Fan(@hwfan)
# Date: Dec 25, 2019
# Last Update: Mar 23, 2020
import time
import sys
def format_size(bytes):
    try:
        bytes = float(bytes)
        KB = bytes / 1024
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
        
def save_response_content(response, filename):
    CHUNK_SIZE = 32768
    total = 0
    start_time = time.time()
    with open(filename, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                interval = time.time()-start_time
                total += len(chunk)
                speed = total/interval
                sys.stdout.write('Downloaded: '+format_size(total).ljust(11, ' ')+'\tSpeed: '+(format_size(speed)+'/s').ljust(13, ' '))
                sys.stdout.flush()
                sys.stdout.write('\r')
    sys.stdout.write('\n')
    # print(total)