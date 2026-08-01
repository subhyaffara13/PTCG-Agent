
def is_executable_in_cache(backend, cache_key: str) -> bool:
  """Checks if the executable is in the cache."""
  cache = _get_cache(backend)
  if cache is None:
    return False

  # TODO(patrios): add check cache key method to cache interface.
  executable_and_time = cache.get(cache_key)
  return executable_and_time is not None

