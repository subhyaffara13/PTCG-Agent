
def get_scalar_handler() -> type_handlers.ScalarHandler:
  """Returns the TypeHandler for scalars."""
  if multihost.is_pathways_backend():
    return pathways_handler_registry.get_pathways_scalar_handler()
  return type_handlers.ScalarHandler()

