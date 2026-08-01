
def _create_v0_scalar_handler() -> type_handlers_v0.ScalarHandler:
  """Creates a V0 ScalarHandler."""
  return registration.get_scalar_handler()

