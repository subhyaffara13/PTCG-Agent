
def _cache_dir_prefix(options: Options) -> str:
    """Get current cache directory (or file if id is given)."""
    if options.bazel:
        # This is needed so the cache map works.
        return os.curdir
    cache_dir = options.cache_dir
    pyversion = options.python_version
    base = os_path_join(cache_dir, "%d.%d" % pyversion)
    return base

