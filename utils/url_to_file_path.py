
def url_to_file_path(url: str, filecache: FileCache) -> str:
    """Return the file cache path based on the URL.

    This does not ensure the file exists!
    """
    key = CacheController.cache_url(url)
    return filecache._fn(key)


def url_to_file_path(url: str, filecache: FileCache) -> str:
    """Return the file cache path based on the URL.

    This does not ensure the file exists!
    """
    key = CacheController.cache_url(url)
    return filecache._fn(key)

