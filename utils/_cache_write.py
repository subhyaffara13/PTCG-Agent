import logging
from typing import Any

def _cache_write(cache_key: str,
                 compile_time_secs: float,
                 module_name: str,
                 backend: xc.Client, executable: xc.LoadedExecutable,
                 host_callbacks: Sequence[Any]) -> None:
  """Writes the `serialized_computation` and its compilation time to the
  persistent compilation cache repository.
  """
  # Only write cache entries from the first process. Otherwise we create
  # problems with contention for writes on some filesystems, e.g., GCS.
  log_priority = (logging.WARNING
                  if config.explain_cache_misses.value
                  and compilation_cache.is_persistent_cache_enabled()
                  else logging.DEBUG)
  if distributed.global_state.process_id != 0:
    logger.log(log_priority,
               "Not writing persistent cache entry since process_id != 0")
    return

  if host_callbacks:
    logger.log(
        log_priority,
        "Not writing persistent cache entry for '%s' because it uses host "
        "callbacks (e.g. from jax.debug.print or breakpoint)", module_name)
    return

  min_compile_time = config.persistent_cache_min_compile_time_secs.value
  if compile_time_secs < min_compile_time:
    logger.log(
        log_priority,
        "Not writing persistent cache entry for '%s' because it took < %.2f "
        "seconds to compile (%.2fs)", module_name, min_compile_time,
        compile_time_secs)
    return
  else:
    logger.debug(
        "'%s' took at least %.2f seconds to compile (%.2fs)",
        module_name, min_compile_time, compile_time_secs)

  try:
    compilation_cache.put_executable_and_time(
        cache_key, module_name, executable, backend, int(compile_time_secs))
  except Exception as ex:
    if _should_raise_persistent_cache_error(ex):
      raise
    warnings.warn(
        f"Error writing persistent compilation cache entry for "
        f"'{module_name}': {type(ex).__name__}: {ex}")

