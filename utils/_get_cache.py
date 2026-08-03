import logging

def _get_cache(backend) -> CacheInterface | None:
  # TODO(b/289098047): consider making this an API and changing the callers of
  # get_executable_and_time() and put_executable_and_time() to call get_cache()
  # and passing the result to them.
  if backend.runtime_type in _UNSUPPORTED_RUNTIMES:
    log_priority = (logging.WARNING if is_persistent_cache_enabled()
                    else logging.DEBUG)
    logger.log(log_priority, "_get_cache: Unsupported runtime: %s",
               backend.runtime_type)
    return None
  if _cache is None:
    _initialize_cache()  # initialization is done at most once; see above
  return _cache

