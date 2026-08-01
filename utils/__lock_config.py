
def _LockConfig(config):
  """Calls config.lock() if config has a lock method."""
  if isinstance(config, _ErrorConfig):
    pass  # Attempting to access _ErrorConfig.lock will raise its error.
  elif getattr(config, 'lock', None) and callable(config.lock):
    config.lock()
  else:
    pass  # config.lock() does not have desired semantics, do nothing.

