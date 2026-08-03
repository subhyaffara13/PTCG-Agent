import os

def atomic_write(path: str, mode: str = "wb"):
    """
    A context manager that opens a temporary file next to `path` and, on exit,
    replaces `path` with the temporary file, thereby updating `path`
    atomically.
    """
    fd, fn = tempfile.mkstemp(
        dir=os.path.dirname(path), prefix=os.path.basename(path) + "-"
    )
    try:
        with open(fd, mode) as fp:
            yield fp
    except BaseException:
        with contextlib.suppress(FileNotFoundError):
            os.unlink(fn)
        raise
    else:
        os.replace(fn, path)

