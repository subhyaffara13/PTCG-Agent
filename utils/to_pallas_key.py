
def to_pallas_key(key: jax.Array) -> jax.Array:
  """Helper function for converting non-Pallas PRNG keys into Pallas keys."""
  # Handle new-style typed PRNG keys.
  generate_key = functools.partial(
      jax.random.bits, shape=tpu_key_impl.key_shape, dtype=jnp.uint32
  )
  vmapped_key = False
  if jnp.issubdtype(key.dtype, dtypes.prng_key):  # New-style typed PRNG key.
    if len(key.shape) > 0:
      vmapped_key = True
  else:  # Legacy uint32 key.
    if len(key.shape) > 1:
      vmapped_key = True

  if vmapped_key:
    pallas_key_data = jax.vmap(generate_key)(key)
  else:
    pallas_key_data = generate_key(key)
  return jax_api_random.wrap_key_data(pallas_key_data, impl="pallas_tpu")

