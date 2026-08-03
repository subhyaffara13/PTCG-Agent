import copy

def _resolve_compilation_strategy(
    computation: ir.Module,
    devices: np.ndarray,
    compile_options: xc.CompileOptions,
    backend: xc.Client,
    pgle_profiler: profiler.PGLEProfiler | None,
    is_multi_process: bool,
    module_name: str,
    min_device_process_id: int,
) -> tuple[str | None, xc.CompileOptions]:
  is_auto_pgle_used = (
      config.enable_pgle.value and config.pgle_profiling_runs.value > 0
  )

  get_cache_key = partial(_get_cache_key, backend=backend,
                          computation=computation, devices=devices)

  if is_auto_pgle_used or config.compilation_cache_expect_pgle.value:
    # This can be None if cache key generation fails.
    pgle_optimized_cache_key = get_cache_key(compile_options,
                                             override_fdo_profile=b"pgle profiled")
    # TODO(b/376647494): remove the workaround when the bug is fixed; the JAX
    # profiler cannot collect sufficiently detailed profile data for PGLE if
    # command buffers / CUDA graphs are enabled. Therefore disable command
    # buffers when compiling for PGLE data collection, but not if AutoPGLE is
    # not enabled, and not when re-compiling using PGLE data. This condition
    # includes `compilation_cache_expect_pgle` so that slow-to-compile modules
    # that are not executed often enough to trigger re-compilation will still
    # be cached between an "enable_pgle" run and an "expect_pgle" run.
    first_pass_compile_options = copy.deepcopy(compile_options)
    first_pass_compile_options.env_option_overrides += [
      ("xla_gpu_enable_command_buffer", ""),
    ]
  else:
    pgle_optimized_cache_key = None
    first_pass_compile_options = compile_options

  # This can be None if cache key generation fails or caching is disabled
  cache_key = get_cache_key(first_pass_compile_options)

  if cache_key is not None and pgle_optimized_cache_key is not None:
    # The compilation cache is enabled and AutoPGLE is enabled/expected
    if _is_executable_in_cache(backend, pgle_optimized_cache_key):
      if config.compilation_cache_expect_pgle.value:
        logger.info(f"PGLE-optimized {module_name} loaded from compilation cache")
      # No need to record N profiles in this case
      if pgle_profiler is not None:
        pgle_profiler.disable()
      return pgle_optimized_cache_key, compile_options
    elif (config.compilation_cache_expect_pgle.value
          and _is_executable_in_cache(backend, cache_key)):
      # No PGLE-optimized module found in the persistent cache, and the user
      # asserted (expect_pgle) that this miss was unexpected
      warnings.warn(f"PERSISTENT CACHE MISS for PGLE-optimized {module_name} "
                    "despite non-PGLE hit; it may not have been executed "
                    "enough times when the cache was populated")

  if (is_auto_pgle_used
      and compile_options.executable_build_options.fdo_profile is not None
      and len(compile_options.executable_build_options.fdo_profile)):
    # Profile data are available to trigger a PGLE-optimized recompilation;
    # store under `pgle_optimized_cache_key` if the cache is enabled
    if is_multi_process and distributed.global_state.client is not None:
      compile_options.executable_build_options.fdo_profile = (
        _share_fdo_profiles(
            computation,
            devices,
            compile_options,
            backend,
            distributed.global_state.client,
            min_device_process_id,
        )
      )
    return pgle_optimized_cache_key, compile_options
  else:
    # Compile for PGLE collection, store under `cache_key` if the cache is
    # enabled. This is also the AutoPGLE-disabled path.
    return cache_key, first_pass_compile_options

