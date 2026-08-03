import os

def _is_parent(dir_a, dir_b):
    """
    Return True if a is a parent of b.
    """
    return os.path.normcase(dir_a).startswith(os.path.normcase(dir_b))

