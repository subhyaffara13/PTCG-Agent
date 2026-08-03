from typing import Any

def _validate_config(config: dict[str, Any]) -> None:
  """Performs basic validation on the loaded YAML config."""
  required_keys = ['suite_name', 'benchmarks']
  for key in required_keys:
    if key not in config:
      raise ValueError(f'Missing required key in YAML config: {key}')

  if not isinstance(config['benchmarks'], list):
    raise ValueError("'benchmarks' must be a list.")

  for i, benchmark_group in enumerate(config['benchmarks']):
    if not isinstance(benchmark_group, dict):
      raise ValueError(
          "Each item in 'benchmarks' must be a dict, got"
          f' {type(benchmark_group)} at index {i}'
      )
    if 'generator' not in benchmark_group:
      raise ValueError(f"Missing 'generator' in benchmarks entry at index {i}")
    if 'options' not in benchmark_group:
      raise ValueError(f"Missing 'options' in benchmarks entry at index {i}")
    if not isinstance(benchmark_group['options'], dict):
      raise ValueError(
          f"'options' must be a dict in benchmarks entry at index {i}"
      )
    options = benchmark_group['options']
    if options.get('capture_digests_path') and options.get(
        'reference_digests_path'
    ):
      raise ValueError(
          'capture_digests_path and reference_digests_path are mutually'
          f' exclusive in benchmarks entry at index {i}: a run either captures'
          ' digests or compares against them.'
      )

