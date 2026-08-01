
def current_trace():
  """Returns the current JAX state tracer."""
  if jax.__version_info__ <= (0, 4, 33):
    top = jax.core.find_top_trace(())
    if top:
      return top.level
    else:
      return float('-inf')

  try:
    # JAX v0.10.0 and newer
    get_opaque_trace_state = jex_core.get_opaque_trace_state
  except AttributeError:
    # JAX v0.9.2 and older
    get_opaque_trace_state = jax.core.get_opaque_trace_state
  return get_opaque_trace_state(convention="flax")

