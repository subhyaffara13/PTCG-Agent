
def _is_tf_installed() -> bool:
  """Checks whether TensorFlow is installed."""
  if not _epath_use_tf():
    return False
  return importlib.util.find_spec('tensorflow') is not None

