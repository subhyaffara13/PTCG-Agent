import os

def _stat_local(path: str) -> tuple[int, float] | None:
    """Stat a local file and return (size, mtime_ms).

    Returns None if the path is missing or is a directory. Uses a single
    ``os.stat`` call so callers don't pay for multiple syscalls per file.
    """
    try:
        st = os.stat(path)
    except OSError:
        return None
    if stat.S_ISDIR(st.st_mode):
        return None
    return st.st_size, st.st_mtime * 1000

