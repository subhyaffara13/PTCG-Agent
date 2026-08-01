
def _get_mtime(name: str) -> float:
    try:
        s = os.stat(name)
        return s.st_mtime
    except OSError as err:
        if err.errno not in {errno.ENOENT, errno.ENOTDIR}:
            raise
    return -1.0

