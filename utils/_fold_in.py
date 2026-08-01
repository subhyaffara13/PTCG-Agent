
def _fold_in(key: jax_prng.PRNGKeyArray, data: typing.Array):
  key0, key1 = unwrap_pallas_seed(key)
  # Perform a cheap mixing of data into the key.
  key1 = key1 + data
  [key0, key1] = threefry2x32.apply_round([key0, key1], 13)
  return wrap_pallas_seed(key0, key1, impl="pallas_tpu")

