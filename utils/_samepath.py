import os

def _samepath(path1, path2):
    # TODO on python3+, there's os.path.samefile
    path1 = os.path.normcase(os.path.abspath(os.path.realpath(path1)))
    path2 = os.path.normcase(os.path.abspath(os.path.realpath(path2)))
    return path1 == path2

