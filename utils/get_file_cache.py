
def get_file_cache(path: str) -> tuple[CacheInterface, str] | None:
  """Returns the file cache and the path to the cache."""
  max_size = config.compilation_cache_max_size.value
  cache = LRUCache(path, max_size=max_size)
  if config.compilation_cache_check_contents.value:
    return VerificationCache(cache), path
  return cache, path

