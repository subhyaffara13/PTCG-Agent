import os

def strip_module(filename):
    if '.' in filename:
        filename = os.path.splitext(filename)[0]
    filename = filename.removesuffix('module')
    return filename

