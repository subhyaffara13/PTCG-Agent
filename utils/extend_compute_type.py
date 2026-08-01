
def extend_compute_type(c_type: str | None):
  if c_type is None:
    yield
    return

  prev = config.compute_on_context_manager.swap_local(c_type)
  try:
    yield c_type
  finally:
    config.compute_on_context_manager.set_local(prev)

