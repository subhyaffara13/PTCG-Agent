
def record_scalar(
    event: str, value: float | int, **kwargs: str | int
) -> None:
  """Record a scalar summary value."""
  for callback in _scalar_listeners:
    callback(event, value, **kwargs)

