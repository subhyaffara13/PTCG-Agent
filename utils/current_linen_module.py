
def current_linen_module() -> linen.Module | None:
  """Get the current Linen module from the Linen context."""
  if linen.module._context.module_stack:  # pylint: disable=W0212
    return linen.module._context.module_stack[-1]  # pylint: disable=W0212
  return None

