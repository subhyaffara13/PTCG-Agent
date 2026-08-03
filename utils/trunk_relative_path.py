import os

def trunk_relative_path(relative):
    return os.path.normpath(os.path.join(trunk_dir, relative))

