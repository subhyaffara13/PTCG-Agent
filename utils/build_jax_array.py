
def build_jax_array(
    array: jax.Array,
    shape: tuple[int, ...],
    result_specs: jax.ShapeDtypeStruct,
) -> jax.Array:
  """Builds a jax.Array."""
  del array
  zeros = jnp.zeros(shape, dtype=jnp.float32)
  return jax.make_array_from_callback(
      shape, result_specs.sharding, lambda idx: zeros[idx], dtype=jnp.float32
  )

