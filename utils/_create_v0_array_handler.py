
def _create_v0_array_handler(
    context: context_lib.Context,
) -> type_handlers_v0.ArrayHandler:
  """Creates a V0 array handler from a V1 context."""
  return registration.get_array_handler(context)

