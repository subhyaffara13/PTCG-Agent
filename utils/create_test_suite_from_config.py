import logging

def create_test_suite_from_config(
    config_path: str,
    output_dir: str | None = None,
    local_directory: str | None = None,
    remove_repeated_dir: bool = False,
) -> core.TestSuite:
  """Loads a benchmark YAML config and builds its TestSuite.

  Perf baseline capture/compare paths (`baseline_capture_path` /
  `baseline_path`) and each load benchmark's correctness-digest paths
  (`capture_digests_path` / `reference_digests_path`, under a benchmark's
  `options`) are read from the config itself — there is no run-flag override.

  Args:
    config_path: Path to the YAML configuration file.
    output_dir: Optional directory to store benchmark results in. If None,
      results will be stored in a temporary directory.
    local_directory: Optional local directory for benchmark results. This is
      used for ECM benchmarks.
    remove_repeated_dir: Whether to remove the generated repeat_* directories
      after execution.

  Returns:
    A TestSuite object containing all benchmarks generated from the config.
  """
  config = load_config(config_path)
  suite_name = config['suite_name']
  num_repeats = config.get('num_repeats', 1)
  checkpoint_configs = _parse_checkpoint_configs(config)
  mesh_configs = _parse_mesh_configs(config)
  baseline_capture_path = config.get('baseline_capture_path')
  baseline_path = config.get('baseline_path')

  generators: list[core.BenchmarksGenerator] = []

  for i, benchmark_group in enumerate(config['benchmarks']):
    generator_class_path = benchmark_group['generator']
    logging.info(
        'Processing benchmark group %d: %s', i + 1, generator_class_path
    )
    try:
      generator_class = _import_class(generator_class_path)
    except ImportError as e:
      logging.error('Failed to import generator class: %s', e)
      raise

    if not issubclass(generator_class, core.BenchmarksGenerator):
      raise TypeError(
          f'Class {generator_class_path} is not a subclass of'
          ' BenchmarksGenerator.'
      )

    options_class = generator_class.options_class
    if options_class is None:
      raise TypeError(
          f'Generator class {generator_class_path} is not decorated with'
          ' @benchmark_options.'
      )

    generator_options_dict = benchmark_group['options']
    try:
      generator_options = options_class.from_dict(generator_options_dict)
    except TypeError as e:
      logging.error(
          'Failed to instantiate options class %s with provided options %s: %s',
          options_class.__name__,
          generator_options_dict,
          e,
      )
      raise

    generator = generator_class(
        checkpoint_configs=checkpoint_configs,
        options=generator_options,
        output_dir=output_dir,
        mesh_configs=mesh_configs,
        local_directory=local_directory,
    )
    generators.append(generator)

  return core.TestSuite(
      name=suite_name,
      benchmarks_generators=generators,
      num_repeats=num_repeats,
      output_dir=output_dir,
      local_directory=local_directory,
      remove_repeated_dir=remove_repeated_dir,
      baseline_path=baseline_path,
      baseline_capture_path=baseline_capture_path,
  )

