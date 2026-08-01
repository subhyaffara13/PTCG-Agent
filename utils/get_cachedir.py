
def get_cachedir():
    """
    Return the string path of the cache directory.

    The procedure used to find the directory is the same as for
    `get_configdir`, except using ``$XDG_CACHE_HOME``/``$HOME/.cache`` instead
    on Linux.  On Windows, uses ``%LOCALAPPDATA%\\matplotlib`` (same as config).
    """
    return _get_config_or_cache_dir(_get_xdg_cache_dir)

