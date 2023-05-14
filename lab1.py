
import sys
import os
import re
import shutil
from urllib.parse import urlparse, unquote
from urllib.request import urlretrieve

name_from_disp = re.compile(r'filename="(.+)"')

def output_progress(blocks, block_size, total_size):
    width = min(os.get_terminal_size().columns - 5, 95)
    percent = min(blocks*block_size, total_size)/total_size
    hyphen_cnt = int(width * percent)
    progress = "[" + '-' * hyphen_cnt + ' ' * (width - hyphen_cnt) + '] '
    print("\r" + progress + str(int(percent*100)) + "%", end="")

def get_filename(url, headers):
    url_name = os.path.basename(urlparse(url).path)
    try:
        headers_name = re.search(name_from_disp, headers["Content-Disposition"]).groups()[0]
    except:
        headers_name = ''
    return headers_name or url_name

def check_duplicate_path(path: len):
    splitted = path.split(sep=".")
    if len(splitted) == 1:
        name = splitted[0]
        ext = ""
    else:
        name = ""
        for i in range(len(splitted) - 2):
            name += splitted[i] + "."
        name += splitted[-2]
        ext = splitted[-1]
    buff_path = path
    i = 1
    while os.path.exists(buff_path):
        buff_path = name + f' ({i}).' + ext
        i += 1
    return buff_path

if __name__ == '__main__':
    url = sys.argv[1]

    path, msg = urlretrieve(url, reporthook=output_progress)
    sys.stdout.write("\n")
    name = unquote(get_filename(url, msg))
    out_path = os.path.dirname(os.path.realpath(sys.argv[0])) + '\\' + name
    out_path = check_duplicate_path(out_path)
    shutil.move(path, out_path)
