
def _compile_and_write_cache(
    backend: xc.Client,
    computation: ir.Module,
    executable_devices: xc.DeviceList,
    compile_options: xc.CompileOptions,
    host_callbacks: Sequence[Any],
    module_name: str,
    cache_key: str,
) -> xc.LoadedExecutable:
  start_time = time.monotonic()
  executable = backend_compile_and_load(
      backend, computation, executable_devices, compile_options, host_callbacks
  )
  compile_time = time.monotonic() - start_time
  _cache_write(
      cache_key, compile_time, module_name, backend, executable, host_callbacks
  )
  return executable

