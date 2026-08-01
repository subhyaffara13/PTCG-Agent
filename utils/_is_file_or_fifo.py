
def _is_file_or_fifo(path: StrPath) -> bool:
    """
    Return True if `path` exists and is either a regular file or a FIFO.
    """
    if os.path.isfile(path):
        return True

    try:
        st = os.stat(path)
    except (FileNotFoundError, OSError):
        return False

    return stat.S_ISFIFO(st.st_mode)

