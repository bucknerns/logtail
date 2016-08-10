from time import sleep
from fnmatch import fnmatch
import os
import sys

file_tracker = {}


def register_existing_files(search_path, name_match="*.log"):
    for path, dirs, files in os.walk(search_path):
        for f in files:
            if name_match is not None and not fnmatch(f, name_match):
                continue
            file_path = os.path.join(path, f)
            size = get_file_size(file_path)
            file_tracker[file_path] = size


def get_newest_file(search_path, name_match="*.log"):
    current_time = 0
    current_file = None
    for path, dirs, files in os.walk(search_path):
        for f in files:
            if name_match is not None and not fnmatch(f, name_match):
                continue
            file_path = os.path.join(path, f)
            mtime = os.stat(file_path).st_mtime
            if mtime > current_time:
                current_time = mtime
                current_file = file_path
    return current_file


def get_file_size(path):
    return os.stat(path).st_size


def print_latest(current_file, size):
    if current_file in file_tracker:
        old_size = file_tracker[current_file]
        if size < old_size:
            print("File Truncated:", current_file)
            old_size = 0
        if old_size != size:
            with open(current_file, "rb") as f:
                f.seek(old_size)
                sys.stdout.write(f.read(size - old_size))
            file_tracker[current_file] = size
    else:
        with open(current_file, "rb") as f:
            sys.stdout.write(f.read(size))
            file_tracker[current_file] = size


def get_file():
    file_ = get_newest_file(*sys.argv[1:])
    size = get_file_size(file_)
    return file_, size


def logtail():

    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print "Usage: taillogs <path> [<file glob>]"
        exit(1)

    register_existing_files(sys.argv[1])
    current_file, size = get_file()
    file_tracker[current_file] = size
    while True:
        current_file, size = get_file()
        print_latest(current_file, size)
        sleep(0.01)


def editlatest():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print "Usage: taillogs <path> [<file glob>]"
        exit(1)
    for editor in ["xdg-open", "subl", "vim", "vi", "nano", "pico"]:
        ret_code = os.system("{0} {1}".format(
            os.getenv('EDITOR', editor), get_newest_file(*sys.argv[1:])))
        if not ret_code:
            return ret_code

if __name__ == "__main__":
    logtail()
