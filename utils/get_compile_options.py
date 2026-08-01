
def get_compile_options(
    num_replicas: int,
    num_partitions: int,
    device_assignment=None,
    env_options_overrides: dict[str, str] | None = None,
    fdo_profile: bytes | None = None,
    detailed_logging: bool = True,
    backend: xc.Client | None = None,
) -> xc.CompileOptions:
  """Returns the compile options to use, as derived from flag values.

  Args:
    num_replicas: Number of replicas for which to compile.
    num_partitions: Number of partitions for which to compile.
    device_assignment: Optional ndarray of jax devices indicating the assignment
      of logical replicas to physical devices (default inherited from
      xla_client.CompileOptions). Must be consistent with `num_replicas` and
      `num_partitions`.
    env_options_overrides: dict of additional options parsed by the compiler
    fdo_profile: Optional profile for feedback-directed optimization passed to
      XLA.
    detailed_logging: Is this an "interesting" computation about which XLA would
      be wise to log compilation information?
    backend: the client, if available.
  """
  compile_options = xc.CompileOptions()
  compile_options.num_replicas = num_replicas
  compile_options.num_partitions = num_partitions
  build_options = compile_options.executable_build_options
  build_options.use_spmd_partitioning = True
  build_options.use_shardy_partitioner = config.use_shardy_partitioner.value
  if fdo_profile is not None:
    build_options.fdo_profile = fdo_profile
  if device_assignment is not None:
    logger.debug(
        'get_compile_options: num_replicas=%s num_partitions=%s device_assignment=%s',
        num_replicas, num_partitions, device_assignment)
    device_assignment = np.array(device_assignment)

    # Allow 1D device assignment if num_partitions is 1.
    if (device_assignment.ndim == 1) and (num_partitions == 1):
      device_assignment = device_assignment[:, None]

    if num_replicas != device_assignment.shape[0]:
      msg = 'device_assignment does not match num_replicas: {} vs {}.'
      raise ValueError(msg.format(device_assignment, num_replicas))

    if num_partitions != device_assignment.shape[1]:
      msg = 'device_assignment does not match num_partitions: {} vs {}.'
      raise ValueError(msg.format(device_assignment, num_partitions))

    if device_assignment.dtype == object:
      device_assignment = np.vectorize(lambda d: d.id, otypes=[int])(
          device_assignment)
    device_assignment = xc.DeviceAssignment.create(device_assignment)
    assert device_assignment.replica_count() == num_replicas
    assert device_assignment.computation_count() == num_partitions
    compile_options.device_assignment = device_assignment

  build_options.exec_time_optimization_effort = config.exec_time_optimization_effort.value
  build_options.memory_fitting_effort = config.memory_fitting_effort.value
  build_options.optimization_level = config.EffortLevel(
      config.optimization_level.value
  ).value
  build_options.memory_fitting_level = config.EffortLevel(
      config.memory_fitting_level.value
  ).value

  if env_options_overrides is not None:
    # Some overrides are passed directly on build_options.
    overrides_on_build_options = [
        "exec_time_optimization_effort", "memory_fitting_effort"]
    overrides_on_build_options.extend(
        ["optimization_level", "memory_fitting_level"]
    )

    env_options_overrides = dict(env_options_overrides)
    for name in overrides_on_build_options:
      if name in env_options_overrides:
        setattr(build_options, name, env_options_overrides.pop(name))
    compile_options.env_option_overrides = list(env_options_overrides.items())

  debug_options = compile_options.executable_build_options.debug_options
  if lib.cuda_path is not None:
    debug_options.xla_gpu_cuda_data_dir = lib.cuda_path

  if _DISABLE_MOST_OPTIMIZATIONS.value:
    debug_options.xla_backend_optimization_level = 0
    debug_options.xla_llvm_disable_expensive_passes = True
    debug_options.xla_test_all_input_layouts = False

  if not config.enable_remat_opt_pass.value:
    debug_options.xla_disable_hlo_passes = "rematerialization"

  # XLA-AutoFDO profile version: precedence order is:
  # 1. Whatever --jax_xla_profile_version is set to.
  # 2. If --jax_xla_profile_version is not set (i.e., 0), call the function
  #    set in get_latest_profile_version and use the return value if non-zero.
  #    If the function returns 0, set -1; this is an error.
  # -1 indicates that no attempt should be made to retrieve the latest profile
  # later on.
  jax_xla_profile_version = config.jax_xla_profile_version.value
  if jax_xla_profile_version > 0:
    compile_options.profile_version = jax_xla_profile_version
    logger.debug("get_compile_options XLA-AutoFDO profile: " +
                 "using JAX XLA profile version %d from flag",
                 jax_xla_profile_version)
  else:
    compile_options.profile_version = _NO_PROFILE_DONT_RETRIEVE
    if backend is None:
      logger.info("get_compile_options: no backend supplied; "
                   "disabling XLA-AutoFDO profile")
    else:
      fdo_profile_version = get_latest_profile_version(backend)
      if fdo_profile_version != 0:
        compile_options.profile_version = fdo_profile_version
        logger.debug("get_compile_options XLA-AutoFDO profile: " +
                     "using XLA-AutoFDO profile version %d",
                     fdo_profile_version)
      else:
        logger.error("get_compile_options XLA-AutoFDO profile: " +
                     "XLA-AutoFDO profile version is 0; this should not happen")

  debug_options.xla_detailed_logging = detailed_logging

  # If persistent cache is enabled, also enable additional XLA caching features.
  if compilation_cache.is_persistent_cache_enabled():
    # compilation_cache_dir can't be None here, but the type checker is a bit
    # strict.
    path = pathlib.Path(config.compilation_cache_dir.value or "")
    enabled_flags = config.persistent_cache_enable_xla_caches.value or ""

    if enabled_flags == "all" or "xla_gpu_kernel_cache_file" in enabled_flags:
      kernel_cache_path = path / "xla_gpu_kernel_cache_file"
      debug_options.xla_gpu_kernel_cache_file = str(kernel_cache_path)
      # This option is required to use the kernel cache.
      debug_options.xla_gpu_enable_llvm_module_compilation_parallelism = True
      logger.debug("Enabling XLA kernel cache at '%s'", kernel_cache_path)

    if enabled_flags == "all" or "xla_gpu_per_fusion_autotune_cache_dir" in enabled_flags:
      autotune_cache_path = path / "xla_gpu_per_fusion_autotune_cache_dir"
      debug_options.xla_gpu_per_fusion_autotune_cache_dir = str(autotune_cache_path)
      logger.debug("Enabling XLA autotuning cache at '%s'", autotune_cache_path)

      # Set caching mode so that only process 0 can write to the cache.
      if distributed.global_state.process_id == 0:
        debug_options.xla_gpu_experimental_autotune_cache_mode = xc.AutotuneCacheMode.UPDATE
      else:
        debug_options.xla_gpu_experimental_autotune_cache_mode = xc.AutotuneCacheMode.READ

  return compile_options

