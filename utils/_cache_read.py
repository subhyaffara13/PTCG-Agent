
def _cache_read(
    module_name: str, cache_key: str, compile_options: xc.CompileOptions,
    backend: xc.Client, executable_devices: xc.DeviceList,
) -> tuple[xc.LoadedExecutable | None, int | None]:
  """Looks up the `computation` and it's compilation time in the persistent
  compilation cache repository.
  """
  try:
    return compilation_cache.get_executable_and_time(
        cache_key, compile_options, backend, executable_devices)
  except Exception as ex:
    if _should_raise_persistent_cache_error(ex):
      raise
    warnings.warn(
        f"Error reading persistent compilation cache entry for "
        f"'{module_name}': {type(ex).__name__}: {ex}")
    return None, None

