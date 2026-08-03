import logging

def log_persistent_cache_hit(module_name: str, cache_key: str) -> None:
  hit_log_priority = (logging.WARNING if config.log_compiles.value
                      else logging.DEBUG)
  logger.log(hit_log_priority, "Persistent compilation cache hit for '%s' with key %r",
             module_name, cache_key)

