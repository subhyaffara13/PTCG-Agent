
def record_event_time_span(
    event: str, start_time: float, end_time: float, **kwargs: str | int
) -> None:
  """Record an event start and end time in seconds (float)."""
  for callback in _event_time_span_listeners:
    callback(event, start_time, end_time, **kwargs)

