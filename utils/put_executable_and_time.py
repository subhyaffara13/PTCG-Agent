
def put_executable_and_time(
    cache_key: str,
    module_name: str,
    executable: xla_client.LoadedExecutable,
    backend,
    compile_time: int
) -> None:
  """Adds the 'executable' and its compilation time to the cache, possibly
  evicting older entries.
  """
  log_priority = (logging.WARNING
                  if config.explain_cache_misses.value
                  and is_persistent_cache_enabled()
                  else logging.DEBUG)
  cache = _get_cache(backend)
  if cache is None:
    logger.log(log_priority,
               "Not writing persistent cache entry with key %r"
               " since cache is disabled/not initialized", cache_key)
    return

  if hasattr(executable, "serialize") or xla_client._version >= 389:
    serialized_executable = executable.serialize()
  else:
    serialized_executable = backend.serialize_executable(executable)
  executable_and_time = combine_executable_and_time(
      serialized_executable, compile_time)
  executable_and_time = compress_executable(executable_and_time)

  min_entry_size = config.persistent_cache_min_entry_size_bytes.value
  entry_size = len(executable_and_time)
  if entry_size < min_entry_size:
    logger.log(log_priority,
        "Not writing persistent cache entry with key %r since its size"
        " (%d bytes) is less than threshold (%d bytes)", cache_key, entry_size,
        min_entry_size)
  else:
    logger.log(log_priority,
               "Writing %s to persistent compilation cache with key %r",
               module_name, cache_key)
    monitoring.record_event('/jax/compilation_cache/cache_misses')
    if config.compilation_cache_expect_pgle.value:
      # User asserted that the compilation cache would already contain PGLE-optimized
      # executables. Because of the size/compile-time thresholds, it is expected that
      # some compilation of small modules will still happen, but that should not lead
      # to compilation cache writes.
      warnings.warn(
          f"PERSISTENT CACHE WRITE with key {cache_key}, this is unexpected because "
          "JAX_COMPILATION_CACHE_EXPECT_PGLE is set. The execution that populated the "
          "cache may lack coverage, "
          "https://docs.jax.dev/en/latest/persistent_compilation_cache.html may "
          "help debug why this has happened")

    cache.put(cache_key, executable_and_time)

