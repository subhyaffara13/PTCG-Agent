import os

def create_mirror_file_if_missing(mirror_file, notebook, fmt):
    if not os.path.isfile(mirror_file):
        write(notebook, mirror_file, fmt=fmt)

