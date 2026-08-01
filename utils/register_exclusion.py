
def register_exclusion(path):
  """Marks a Flax source file for exclusion."""
  global _flax_exclusions, _flax_filter_tracebacks
  # Record flax exclusions so we can dynamically add and remove them.
  _flax_exclusions.add(path)
  if _flax_filter_tracebacks:
    jax_traceback_util.register_exclusion(path)
    source_info_util.register_exclusion(path)


def register_exclusion(path: str):
  _exclude_paths.append(path)
  _exclude_path_regex.cache_clear()
  is_user_filename.cache_clear()


def register_exclusion(path: str):
  _exclude_paths.append(path)
  _jax.add_exclude_path(path)

