import os
from pathlib import Path


def try_makedirs(cache_dir: Path) -> bool:
    """Attempt to create the given directory and sub-directories exist.

    Returns True if successful or if it already exists.
    """
    try:
        os.makedirs(cache_dir, exist_ok=True)
    except (FileNotFoundError, NotADirectoryError, FileExistsError):
        # One of the path components was not a directory:
        # - we're in a zip file
        # - it is a file
        return False
    except PermissionError:
        return False
    except OSError as e:
        # as of now, EROFS doesn't have an equivalent OSError-subclass
        #
        # squashfuse_ll returns ENOSYS "OSError: [Errno 38] Function not
        # implemented" for a read-only error
        if e.errno in {errno.EROFS, errno.ENOSYS}:
            return False
        raise
    return True

