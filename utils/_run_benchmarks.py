import logging

def _run_benchmarks(
    config_file: str,
    output_directory: str,
    local_directory: str | None = None,
    remove_repeated_dir: bool = False,
) -> None:
  """Runs Orbax checkpoint benchmarks based on a generator class and a config file.

  Args:
    config_file: Path to the YAML configuration file.
    output_directory: Directory to store benchmark results in.
    local_directory: Local directory for benchmark results. This is used for ECM
      benchmarks.
    remove_repeated_dir: Whether to remove the generated repeat_* directories
      after execution.

  Raises:
    RuntimeError: If any benchmark test fails.
  """
  logging.info('Running benchmarks from config: %s', config_file)
  logging.info('Output directory: %s', output_directory)
  try:
    epath.Path(output_directory).mkdir(parents=True, exist_ok=True)
    logging.info('Ensured output directory exists: %s', output_directory)
  except OSError as e:
    logging.exception(
        'Failed to create output directory %s: %s', output_directory, e
    )
    raise

  try:
    test_suite = config_parsing.create_test_suite_from_config(
        config_file,
        output_dir=output_directory,
        local_directory=local_directory,
        remove_repeated_dir=remove_repeated_dir,
    )
  except Exception as e:
    logging.error('Failed to create test suite from config: %s', e)
    raise

  logging.info('Benchmark test suite created successfully.')
  results = test_suite.run()
  failed_results = [result for result in results if not result.is_successful()]
  if not failed_results:
    logging.info('Benchmark test suite run completed successfully.')
  else:
    error_messages = []
    for result in failed_results:
      error_messages.append(
          f'Test: {result.metrics.name}, Error: {repr(result.error)}'
      )
    exception_message = (
        'Benchmark test suite run failed with following errors:\n'
        + '\n'.join(error_messages)
    )
    raise RuntimeError(exception_message)


def _run_benchmarks(
    config_file: str, output_directory: str, remove_repeated_dir: bool = False
) -> None:
  """Runs the benchmarks."""
  logging.info('Running benchmarks from config: %s', config_file)
  logging.info('Output directory: %s', output_directory)

  if dist.get_rank() == 0:
    try:
      epath.Path(output_directory).mkdir(parents=True, exist_ok=True)
      logging.info('Output directory created: %s', output_directory)
    except OSError as e:
      logging.exception('Failed to create output directory: %s', e)
      raise
  dist.barrier()

  try:
    test_suite = config_parsing.create_test_suite_from_config(
        config_file,
        output_dir=output_directory,
        remove_repeated_dir=remove_repeated_dir,
    )
  except Exception as e:
    logging.error('Failed to create test suite from config: %s', e)
    raise

  logging.info('Benchmark test suite created successfully.')
  results = test_suite.run()
  failed_results = [result for result in results if not result.is_successful()]
  if not failed_results:
    logging.info('Benchmark test suite run completed successfully.')
  else:
    error_messages = []
    for result in failed_results:
      error_messages.append(
          f'Test: {result.metrics.name}, Error: {repr(result.error)}'
      )
    exception_message = (
        'Benchmark test suite run failed with following errors:\n'
        + '\n'.join(error_messages)
    )
    raise RuntimeError(exception_message)

