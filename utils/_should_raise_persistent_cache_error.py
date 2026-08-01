
def _should_raise_persistent_cache_error(ex: Exception) -> bool:
  """Returns True if the exception should be raised, False if it should be warned."""
  return (
      config.raise_persistent_cache_errors.value or
      isinstance(ex, compilation_cache.CacheVerificationError)
  )

