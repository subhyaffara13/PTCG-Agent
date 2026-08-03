import os

def _extant(path):
    """
    Replace path with None if it doesn't exist.
    """
    return path if os.path.exists(path) else None

