import copy
import threading
import shutil
import os

def download_session(session_func, url, filename, proc_id, start, end, used_proxy):
    drive_session = session_func(used_proxy)
    drive_session.set_range(start, end)
    drive_session.connect(url, filename)
    drive_session.save_response_content(start=start, proc_id=proc_id)
    
class MultiThreadDownloader:
    def __init__(self, session_func, used_proxy, filesize, thread_number):
        self.session_func = session_func
        self.used_proxy = used_proxy
        self.thread_number = thread_number
        self.filesize = filesize
        self.get_ranges()

    def get_ranges(self):
        self.ranges = []
        offset = int(self.filesize / self.thread_number)
        for i in range(self.thread_number):
            if i == self.thread_number - 1:
                self.ranges.append((str(i * offset), ''))
            else:
                self.ranges.append((str(i * offset), str((i+1) * offset - 1)))
    
    def get(self, url, filename):
        thread_list = []
        for proc_id, each_range in enumerate(self.ranges):
            start, end = each_range
            thread = threading.Thread(target=download_session, args=(self.session_func, url, filename, proc_id, start, end, self.used_proxy))
            thread.start()
            thread_list.append(thread)

        for i in thread_list:
            i.join()
    
    def concatenate(self, filename):
        sub_filenames = []
        dirname = os.path.dirname(filename)
        tmp_dirname = os.path.join(dirname, 'tmp')
        for proc_id in range(len(self.ranges)):
            name, ext = os.path.splitext(filename)
            name = name + '_{}'.format(proc_id)
            sub_filename = name + ext
            sub_basename = os.path.basename(sub_filename)
            sub_filename = os.path.join(tmp_dirname, sub_basename)
            sub_filenames.append(sub_filename)

        with open(filename, 'wb') as wfd:
            for f in sub_filenames:
                with open(f, 'rb') as fd:
                    shutil.copyfileobj(fd, wfd)
                os.remove(f)
        shutil.rmtree(tmp_dirname)
        