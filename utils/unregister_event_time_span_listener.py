
def unregister_event_time_span_listener(
    callback: EventTimeSpanListenerWithMetadata,
) -> None:
  """Unregister an event time span listener by callback."""
  assert callback in _event_time_span_listeners
  _event_time_span_listeners.remove(callback)

