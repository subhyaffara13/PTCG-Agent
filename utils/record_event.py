
def record_event(event_index: int, stream_index: int) -> None:
    event = _get_event_by_index(event_index)
    stream = _get_stream_by_index(stream_index)
    event.record(stream)


def record_event(event: str, **kwargs: str | int) -> None:
  """Record an event.

  If **kwargs are specified, all of the named arguments have to be passed in the
  same order across all invocations of this method for the same event.
  """
  for callback in _event_listeners:
    callback(event, **kwargs)

