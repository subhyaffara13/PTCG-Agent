import logging

def log_persistent_cache_miss(module_name: str, cache_key: str) -> None:
  miss_log_priority = (logging.WARNING
                        if config.explain_cache_misses.value
                        and compilation_cache.is_persistent_cache_enabled()
                        else logging.DEBUG)
  # all caps to match the tracing cache "TRACING CACHE MISS"
  logger.log(miss_log_priority, "PERSISTENT COMPILATION CACHE MISS for '%s' with key %r",
             module_name, cache_key)

