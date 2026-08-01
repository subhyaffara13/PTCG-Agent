
def _key_data(keys: Array) -> Array:
  assert dtypes.issubdtype(keys.dtype, dtypes.prng_key)
  return prng.random_unwrap(keys)

