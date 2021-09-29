# -*- coding: utf-8 -*-
"""
The utility copies the entire directory when a file is added or changed in it.
param 1 - source directory
param 2 - destination directory
"""
import os, sys, time
from distutils.dir_util import copy_tree
from distutils.errors import DistutilsFileError

def get_dir_stat(src):
    ret = []
    for dir, subdir, file in os.walk(src):
        stat = os.stat(dir)
        ret.append((dir, stat.st_mtime))
        for v_file in file:
            # skip temporary files
            if os.path.splitext(v_file)[1] == '.bro':
                continue
            stat = os.stat(os.path.join(dir, v_file))
            ret.append((os.path.join(dir, v_file), stat.st_mtime))
    return ret

def copy_all_files(src, dest, wait = 5):
    try:
        res = copy_tree(str(src), str(dest))
    except DistutilsFileError as e:
        print("Cannot copy a file while downloading {}. Waiting for {} sec...".format(str(e), wait))
        time.sleep(wait)

def show_time(ts):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(ts)))
    
if len(sys.argv) < 3:
    print("You need at least 2 arguments!")
    sys.exit(1)
    
src = sys.argv[1]
dest = sys.argv[2]

print("Your folder path is {}".format(src))
before_stat = get_dir_stat(src)
i = 0
while 1:
    i += 1
    after_stat = get_dir_stat(src)  
    changed = [(f, t) for f, t in after_stat if not (f, t) in before_stat]
    if changed or i == 1:
        for f, t in changed:
            print("Modified: {} in {}".format(f, show_time(t)))
        copy_all_files(src, dest)
        before_stat = after_stat     
    else:
        time.sleep(1)