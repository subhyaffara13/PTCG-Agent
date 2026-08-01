
def _create_v0_numpy_handler() -> type_handlers_v0.NumpyHandler:
  """Creates a V0 `NumpyHandler`."""
  return registration.get_numpy_handler()

