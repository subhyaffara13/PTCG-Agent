
def register_event_time_span_listener(
    callback: EventTimeSpanListenerWithMetadata,
) -> None:
  """Register a callback to be invoked during record_event_time_span()."""
  _event_time_span_listeners.append(callback)

