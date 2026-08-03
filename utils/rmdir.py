import os

def rmdir(path, **opts):
    if os.path.isdir(path):
        rmtree(path, **opts)

