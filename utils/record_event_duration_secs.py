
def record_event_duration_secs(event: str, duration: float,
                               **kwargs: str | int) -> None:
  """Record an event duration in seconds (float).

  If **kwargs are specified, all of the named arguments have to be passed in the
  same order across all invocations of this method for the same event.
  """
  for callback in _event_duration_secs_listeners:
    callback(event, duration, **kwargs)

