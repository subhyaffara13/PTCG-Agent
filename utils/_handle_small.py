
def _handle_small(dtype: jax_typing.DTypeLike):
  """Ugly workaround to support types that don't allow automatic promotion."""
  if dtype == jnp.int4:
    return jnp.int8
  if dtype == jnp.float8_e4m3b11fnuz:
    return jnp.bfloat16
  return dtype

