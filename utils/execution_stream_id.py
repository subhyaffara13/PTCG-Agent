
def execution_stream_id(new_id: int):
  """Context manager that overwrites and restores the current thread's execution_stream_id."""
  saved = _xla.get_execution_stream_id()
  _xla.set_execution_stream_id(new_id)
  try:
    yield
  finally:
    _xla.set_execution_stream_id(saved)

