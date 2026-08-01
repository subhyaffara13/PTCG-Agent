
def unregister_scalar_listener(
    callback: ScalarListenerWithMetadata,
) -> None:
  """Unregister a scalar event listener by callback."""
  assert callback in _scalar_listeners
  _scalar_listeners.remove(callback)

