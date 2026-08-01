
def key_data(keys: ArrayLike) -> Array:
  """Recover the bits of key data underlying a PRNG key array."""
  keys, _ = _check_prng_key("key_data", keys, allow_batched=True)
  return _key_data(keys)

