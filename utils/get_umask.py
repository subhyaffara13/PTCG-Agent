import os

def get_umask(mask: int = 0o666) -> int:
    """Get the current umask.

    Follows https://stackoverflow.com/a/44130549 to get the umask.
    Temporarily sets the umask to the given value, and then resets it to the
    original value.
    """
    value = os.umask(mask)
    os.umask(value)
    return value

