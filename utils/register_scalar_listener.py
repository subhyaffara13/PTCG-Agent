
def register_scalar_listener(
    callback : ScalarListenerWithMetadata,
) -> None:
  """Register a callback to be invoked during record_scalar()."""
  _scalar_listeners.append(callback)

