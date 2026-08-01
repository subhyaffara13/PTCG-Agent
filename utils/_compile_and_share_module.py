
def _compile_and_share_module(
    backend: xc.Client,
    computation: ir.Module,
    executable_devices: xc.DeviceList,
    compile_options: xc.CompileOptions,
    host_callbacks: Sequence[Any],
    global_client: lib._jax.DistributedRuntimeClient,
    module_name: str,
    cache_key: str,
    first_process_id: int
) -> xc.LoadedExecutable:
  share_timeout = config.share_binary_between_hosts_timeout_ms.value

  if cache_key in _compile_and_share_module.modules_cache:  # pyrefly: ignore[missing-attribute]
    return _compile_and_share_module.modules_cache[cache_key]  # pyrefly: ignore[missing-attribute]

  if distributed.global_state.process_id == first_process_id:
    logger.debug("Process %d compiling and sharing module: %s",
                 first_process_id, module_name)
    executable = _compile_and_write_cache(
        backend,
        computation,
        executable_devices,
        compile_options,
        host_callbacks,
        module_name,
        cache_key,
    )
    serialized_executable = backend.serialize_executable(executable)
    serialized_executable = compilation_cache.compress_executable(
        serialized_executable
    )
    global_client.key_value_set_bytes(cache_key, serialized_executable)
  else:
    logger.debug("Waiting for module: %s from process %d", module_name,
                 first_process_id)
    serialized_executable = global_client.blocking_key_value_get_bytes(
        cache_key, share_timeout
    )
    serialized_executable = compilation_cache.decompress_executable(
        serialized_executable
    )
    executable = backend.deserialize_executable(
        serialized_executable, executable_devices, compile_options)

  _compile_and_share_module.modules_cache[cache_key] = executable  # pyrefly: ignore[missing-attribute]
  return executable

