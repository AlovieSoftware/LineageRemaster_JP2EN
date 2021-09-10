import os, sys, time
from distutils.dir_util import copy_tree

def get_dir_stat(src):
    ret = []
    for dir, subdir, file in os.walk(src):
        stat = os.stat(dir)
        ret.append((dir, stat.st_mtime))
        for v_file in file:
            stat = os.stat(os.path.join(dir, v_file))
            ret.append((os.path.join(dir, v_file), stat.st_mtime))
    return ret

def copy_all_files(src, dest):
    res = copy_tree(str(src), str(dest))

def show_time(ts):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(ts)))
    
if len(sys.argv) < 3:
    print("You need at least 2 arguments!")
    sys.exit(1)
    
src = sys.argv[1]
dest = sys.argv[2]

print("Your folder path is {}".format(src))
before_stat = get_dir_stat(src)
while 1:    
    after_stat = get_dir_stat(src)
    changed = [(f, t) for f, t in after_stat if not (f, t) in before_stat]
    if changed:
        for f, t in changed:
            print("Modified: {} in {}".format(f, show_time(t)))
        copy_all_files(src, dest)
        before_stat = after_stat     
    else:
        time.sleep(1)