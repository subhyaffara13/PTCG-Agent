
def unregister_event_listener(
    callback: EventListenerWithMetadata,
) -> None:
  """Unregister an event listener by callback."""
  assert callback in _event_listeners
  _event_listeners.remove(callback)

