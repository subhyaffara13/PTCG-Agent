
def show_flax_in_tracebacks():
  """Shows Flax internal stack frames in tracebacks."""
  global _flax_exclusions, _flax_filter_tracebacks
  _flax_filter_tracebacks = False
  for exclusion in _flax_exclusions:
    if exclusion in jax_traceback_util._exclude_paths:
      jax_traceback_util._exclude_paths.remove(exclusion)

