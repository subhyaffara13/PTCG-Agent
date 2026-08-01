
def get_executable_and_time(
    cache_key: str, compile_options, backend, executable_devices
) -> tuple[xla_client.LoadedExecutable | None, int | None]:
  """Returns the cached executable and its compilation time if present, or None
  otherwise.
  """
  cache = _get_cache(backend)
  if cache is None:
    logger.debug("get_executable_and_time: cache is disabled/not initialized")
    return None, None
  executable_and_time = cache.get(cache_key)
  if executable_and_time is None:
    return None, None

  executable_and_time = decompress_executable(executable_and_time)
  serialized_executable, compile_time = extract_executable_and_time(
      executable_and_time)
  xla_executable_deserialized = backend.deserialize_executable(
      serialized_executable, executable_devices, compile_options)
  return xla_executable_deserialized, compile_time

