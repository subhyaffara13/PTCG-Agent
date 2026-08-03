import time
from typing import Any

def compile_or_get_cached(
    backend: xc.Client,
    computation: ir.Module,
    devices: np.ndarray,
    compile_options: xc.CompileOptions,
    host_callbacks: Sequence[Any],
    executable_devices: xc.DeviceList,
    pgle_profiler: profiler.PGLEProfiler | None = None,
) -> xc.LoadedExecutable:
  sym_name = computation.operation.attributes['sym_name']
  module_name = ir.StringAttr(sym_name).value

  if dumped_to := mlir.dump_module_to_file(computation, "compile"):
    logger.info("Dumped the module to %s.", dumped_to)

  is_multi_process = (
      len({device.process_index for device in devices.flatten()}) > 1
  )
  min_device_process_id = min(
      devices.flatten(), key=lambda device: device.id
  ).process_index

  # cache_key: may be None if compilation caching is disabled
  cache_key, compile_options = _resolve_compilation_strategy(
    computation,
    devices,
    compile_options,
    backend,
    pgle_profiler,
    is_multi_process,
    module_name,
    min_device_process_id,
  )

  if cache_key is None:
    return backend_compile_and_load(
        backend, computation, executable_devices, compile_options,
        host_callbacks)

  monitoring.record_event('/jax/compilation_cache/compile_requests_use_cache')

  cache_retrieval_start = time.monotonic()
  retrieved_executable, retrieved_compile_time = _cache_read(
      module_name, cache_key, compile_options, backend, executable_devices)
  cache_retrieval_time = time.monotonic() - cache_retrieval_start

  if retrieved_executable is not None:
    assert retrieved_compile_time is not None
    log_persistent_cache_hit(module_name, cache_key)

    monitoring.record_event('/jax/compilation_cache/cache_hits')
    monitoring.record_event_duration_secs(
        '/jax/compilation_cache/compile_time_saved_sec',
        retrieved_compile_time - cache_retrieval_time)

    monitoring.record_event_duration_secs(
        "/jax/compilation_cache/cache_retrieval_time_sec", cache_retrieval_time)

    return retrieved_executable
  util.test_event("compile_after_persistent_compilation_miss")
  if (
      config.share_binary_between_hosts.value
      and is_multi_process
      and distributed.global_state.client is not None
      # Host callbacks are currently baked into the HLO module so we can't share
      # them.
      and len(host_callbacks) == 0
  ):
    log_persistent_cache_miss(module_name, cache_key)
    return _compile_and_share_module(
        backend,
        computation,
        executable_devices,
        compile_options,
        host_callbacks,
        distributed.global_state.client,
        module_name,
        cache_key,
        min_device_process_id
    )
  else:
    log_persistent_cache_miss(module_name, cache_key)
    return _compile_and_write_cache(
        backend,
        computation,
        executable_devices,
        compile_options,
        host_callbacks,
        module_name,
        cache_key,
    )

