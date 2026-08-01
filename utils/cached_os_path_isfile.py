
def cached_os_path_isfile(path: str | os.PathLike[str]) -> bool:
    """A cached version of os.path.isfile that helps avoid repetitive I/O"""
    return os.path.isfile(path)

