import os

def _normalize_path(path: str) -> str:
    """Resolve symlinks in path and convert to absolute path.

    Note that environment variables and ~ in the path need to be expanded in
    advance.

    This can be cached by using _cache_normalize_path.
    """
    return os.path.normcase(os.path.realpath(path))


def _normalize_path(path):
    """Normalize a path by ensuring it is a string.

    If the resulting string contains path separators, an exception is raised.
    """
    parent, file_name = os.path.split(path)
    if parent:
        raise ValueError(f"{path!r} must be only a file name")
    else:
        return file_name

