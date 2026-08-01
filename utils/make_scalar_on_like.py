
def make_scalar_on_like(
    value: Any, like: jax.Array, *, dtype: Any
) -> jax.Array:
  """Builds a scalar array on the same global sharding as `like`."""
  return colocated_transport.make_scalar_array_like(value, like, dtype=dtype)

