
def clear_in_memory_compilation_cache() -> None:
  """Clears the in-memory compilation cache.

  This function clears all cached executables that were compiled by
  _cached_compilation function.
  """
  _cached_compilation.cache_clear()

