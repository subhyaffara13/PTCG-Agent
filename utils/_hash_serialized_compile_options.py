import copy

def _hash_serialized_compile_options(hash_obj, compile_options_obj,
                                     strip_device_assignment=False):
  # Do not mess with the original CompileOptions object since it is passed to
  # the compiler. Create a deep copy for the purpose of cache key generation.
  compile_options_copy = copy.deepcopy(compile_options_obj)

  # Certain debug options do not affect the compile result and thus, should not
  # be part of the cache key as their inclusion will result in unnecessary cache
  # misses. Clear them here by setting bool values to False, ints to 0, and
  # strings to empty. The exact values used to clear are not relevant as long
  # as the same values are used every time for each field.
  debug_options = compile_options_copy.executable_build_options.debug_options
  # LINT.IfChange(debug_options)
  debug_options.xla_force_host_platform_device_count = 0
  debug_options.xla_dump_to = ""
  debug_options.xla_dump_hlo_module_re = ""
  debug_options.xla_dump_hlo_pass_re = ""
  debug_options.xla_dump_hlo_as_text = False
  debug_options.xla_dump_hlo_as_proto = False
  debug_options.xla_dump_hlo_as_dot = False
  debug_options.xla_dump_hlo_as_url = False
  debug_options.xla_dump_hlo_as_html = False
  debug_options.xla_dump_fusion_visualization = False
  debug_options.xla_dump_hlo_snapshots = False
  debug_options.xla_dump_max_hlo_modules = False
  debug_options.xla_dump_module_metadata = False
  debug_options.xla_dump_compress_protos = False
  debug_options.xla_dump_hlo_as_long_text = False
  debug_options.xla_dump_disable_metadata = False
  debug_options.xla_dump_hlo_pipeline_re = ""
  debug_options.xla_gpu_experimental_autotune_cache_mode = 0

  # Optional way to specify the cuda install path to be used by the compiler.
  # This could possibly affect the cuda version compiled with, but this should
  # already be included in the platform information (and might not be reflected
  # by the cuda path regardless, since this only hashes on the directory name
  # and not the contents). It can also cause spurious cache misses if the cuda
  # path changes across runs despite being the same version, so we clear it
  # here.
  debug_options.xla_gpu_cuda_data_dir = ""
  # LINT.ThenChange(:xla_flags)

  compile_options_copy.env_option_overrides = [
      flag_value
      for flag_value in compile_options_copy.env_option_overrides
      if flag_value[0] not in env_override_flags_to_exclude_from_cache_key
  ]
  if strip_device_assignment and compile_options_copy.device_assignment:
    replica_count = compile_options_copy.device_assignment.replica_count()
    computation_count = compile_options_copy.device_assignment.computation_count()
    compile_options_copy.device_assignment = xla_client.DeviceAssignment.create(
        np.arange(replica_count * computation_count).reshape(  # pyrefly: ignore[bad-argument-type]
          [replica_count, computation_count])
    )
  return hash_obj.update(compile_options_copy.SerializeAsString())

