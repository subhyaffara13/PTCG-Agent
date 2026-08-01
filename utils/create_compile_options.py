
def create_compile_options(
    computation, tuple_args, allow_prop_to_inputs, allow_prop_to_outputs,
    backend, np_dev, compiler_options):
  num_replicas, num_partitions = 1, np_dev.size
  xla_device_assignment = np_dev.reshape((num_replicas, num_partitions))
  fdo_profile = compiler_options.pop("fdo_profile", None)
  compile_options = compiler.get_compile_options(
      num_replicas=num_replicas,
      num_partitions=num_partitions,
      device_assignment=xla_device_assignment,
      env_options_overrides=compiler_options,
      fdo_profile=fdo_profile,
      detailed_logging=compiler.use_detailed_logging(computation),
      backend=backend,
  )
  opts = compile_options.executable_build_options
  compile_options.parameter_is_tupled_arguments = tuple_args
  opts.allow_spmd_sharding_propagation_to_parameters = list(allow_prop_to_inputs)
  opts.allow_spmd_sharding_propagation_to_output = list(allow_prop_to_outputs)
  return compile_options

