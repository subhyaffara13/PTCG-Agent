import os

def maybe_relative_path(path):
    if not os.path.isabs(path):
        return path      # already relative
    dir = path
    names = []
    while True:
        prevdir = dir
        dir, name = os.path.split(prevdir)
        if dir == prevdir or not dir:
            return path     # failed to make it relative
        names.append(name)
        try:
            if samefile(dir, os.curdir):
                names.reverse()
                return os.path.join(*names)
        except OSError:
            pass

