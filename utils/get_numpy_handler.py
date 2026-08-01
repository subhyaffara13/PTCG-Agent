
def get_numpy_handler() -> type_handlers.NumpyHandler:
  """Returns the TypeHandler for Numpy arrays."""
  if multihost.is_pathways_backend():
    return pathways_handler_registry.get_pathways_numpy_handler()
  return type_handlers.NumpyHandler()

