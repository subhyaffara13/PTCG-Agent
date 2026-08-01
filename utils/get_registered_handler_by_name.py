
def get_registered_handler_by_name(
    registry: CheckpointableHandlerRegistry,
    name: str,
) -> CheckpointableHandler | None:
  """Returns the handler for the given name if registered."""
  if registry.has(name):
    return _construct_handler_instance(name, registry.get(name))
  return None

