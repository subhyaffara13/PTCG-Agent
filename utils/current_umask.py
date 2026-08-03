import os

def current_umask():
    tmp = os.umask(0o022)
    os.umask(tmp)
    return tmp


def current_umask() -> int:
    """Get the current umask which involves having to set it temporarily."""
    mask = os.umask(0)
    os.umask(mask)
    return mask

