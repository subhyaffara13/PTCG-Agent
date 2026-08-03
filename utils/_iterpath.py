import os

def _iterpath(path):
    path, last = os.path.split(path)
    if last:
        yield from _iterpath(path)
        yield last

