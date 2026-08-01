
def current_module() -> Module | None:
  """A quick util to get the current bridge module."""
  ctx = current_context()
  if ctx is None:
    return None
  return ctx.module

