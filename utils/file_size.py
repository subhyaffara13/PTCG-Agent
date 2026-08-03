import os

def file_size(filelike: IO[bytes]) -> int:
    """Find length of any open read-mode file-like"""
    pos = filelike.tell()
    try:
        return filelike.seek(0, 2)
    finally:
        filelike.seek(pos)


def file_size(path: str) -> int | float:
    # If it's a symlink, return 0.
    if os.path.islink(path):
        return 0
    return os.path.getsize(path)

