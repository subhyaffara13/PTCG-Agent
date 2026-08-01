
def create_cache_mapper(same_names: bool) -> AbstractCacheMapper:
    """Factory method to create cache mapper for backward compatibility with
    ``CachingFileSystem`` constructor using ``same_names`` kwarg.
    """
    if same_names:
        return BasenameCacheMapper()
    else:
        return HashCacheMapper()

