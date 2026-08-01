
def _share_fdo_profiles(
    computation: ir.Module,
    devices: np.ndarray,
    compile_options: xc.CompileOptions,
    backend: xc.Client,
    global_client: lib._jax.DistributedRuntimeClient,
    min_process_id
) -> bytes:
  sym_name = computation.operation.attributes['sym_name']
  module_name = ir.StringAttr(sym_name).value
  fdo_profile = compile_options.executable_build_options.fdo_profile
  if len(fdo_profile) == 0:
    return fdo_profile

  compile_options.executable_build_options.fdo_profile = b""
  try:
    profile_key = (
        compilation_cache.get_cache_key(
            computation,
            devices,
            compile_options,
            backend,
            cache_key_type.IgnoreCallbacks.ALL,
        )
        + "_fdo_sync"
    )
  except _jax.JaxRuntimeError as ex:
    logger.error(
        "compile_or_get_cached: unable to generate cache key, "
        "skipping the fdo profile sharing: %s",
        ex,
    )
    return fdo_profile

  if profile_key in _share_fdo_profiles.modules_profiles:  # pyrefly: ignore[missing-attribute]
    return _share_fdo_profiles.modules_profiles[profile_key]  # pyrefly: ignore[missing-attribute]

  share_timeout = config.share_binary_between_hosts_timeout_ms.value
  if distributed.global_state.process_id == min_process_id:
    logger.debug(
        "Module %s. Sharing FDO profile. Process %d.",
        module_name,
        min_process_id,
    )
    global_client.key_value_set_bytes(profile_key, fdo_profile)
  else:
    logger.debug(
        "Module %s. Waiting for FDO profile which should be set by process %d.",
        module_name,
        min_process_id,
    )
    fdo_profile = global_client.blocking_key_value_get_bytes(
        profile_key, share_timeout
    )

  _share_fdo_profiles.modules_profiles[profile_key] = fdo_profile  # pyrefly: ignore[missing-attribute]
  return fdo_profile

