import os
from pathlib import Path


def is_fs_root(p: Path) -> bool:
    r"""
    Return True if the given path is pointing to the root of the
    file system ("/" on Unix and "C:\\" on Windows for example).
    """
    return os.path.splitdrive(str(p))[1] == os.sep

