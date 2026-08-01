
def _convert_floats(x, dtype):
  """Convert float-like inputs to dtype, rest pass through."""
  # if the x is already a strong dtype jax.Array, return unchanged
  if isinstance(x, jax.Array) and not getattr(x, 'weak_type', False):
    return x
  # if x is of floating point type, cast to the specified dtype
  current_dtype = x.dtype if hasattr(x, 'dtype') else type(x)
  if jax.dtypes.issubdtype(current_dtype, jnp.floating):
    return jnp.asarray(x, dtype=dtype)
  # otherwise, pass through unchanged
  return x

