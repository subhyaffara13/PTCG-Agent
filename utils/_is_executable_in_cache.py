
def _is_executable_in_cache(backend, cache_key) -> bool:
  """Checks if executable is presented in cache on a given key
  """
  try:
    return compilation_cache.is_executable_in_cache(backend, cache_key)
  except Exception as ex:
    if _should_raise_persistent_cache_error(ex):
      raise
    warnings.warn(
        f"Error reading persistent compilation cache entry for "
        f"'{cache_key}': {type(ex).__name__}: {ex}")
    return False

