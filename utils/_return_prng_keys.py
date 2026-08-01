
def _return_prng_keys(was_wrapped, key):
  # TODO(frostig): remove once we always enable_custom_prng
  assert dtypes.issubdtype(key.dtype, dtypes.prng_key)
  if config.enable_custom_prng.value:
    return key
  else:
    return prng.random_unwrap(key) if was_wrapped else key

