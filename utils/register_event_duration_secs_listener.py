
def register_event_duration_secs_listener(
    callback : EventDurationListenerWithMetadata) -> None:
  """Register a callback to be invoked during record_event_duration_secs()."""
  _event_duration_secs_listeners.append(callback)

