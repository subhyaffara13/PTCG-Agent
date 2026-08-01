
def current_jax_trace():
  """Returns the Jax tracing state."""
  return jax.extend.core.get_opaque_trace_state(convention="nnx")

