
def canonicalize_key(key_or_seed: jax.Array | int) -> jax.Array:
  """Canonicalize a random key or an int representing a seed to a random key."""
  if (isinstance(key_or_seed, jax.Array) and jnp.issubdtype(
      key_or_seed.dtype, jax.dtypes.prng_key
  )):
    return key_or_seed
  return jax.random.key(key_or_seed)

