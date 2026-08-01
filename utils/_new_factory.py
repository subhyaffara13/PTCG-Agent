
def _new_factory(old_factory, *args, **kwargs) -> py_logging.LogRecord:
  """Update the logs."""
  # TODO(epot): Add color ?
  record = old_factory(*args, **kwargs)
  return record

