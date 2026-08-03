import sys

def insert_shim():
    sys.meta_path.insert(0, DISTUTILS_FINDER)

