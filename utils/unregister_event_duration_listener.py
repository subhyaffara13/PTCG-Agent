
def unregister_event_duration_listener(
    callback: EventDurationListenerWithMetadata,
) -> None:
  """Unregister an event duration listener by callback."""
  assert callback in _event_duration_secs_listeners
  _event_duration_secs_listeners.remove(callback)

