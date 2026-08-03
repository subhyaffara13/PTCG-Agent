import random

def _fold_in_static(
  rng: PRNGKey, data: typing.Collection[PRNGFoldable]
) -> PRNGKey:
  """Folds static data (strings & ints) into a jax.random.PRNGKey using its SHA-1 hash.

  This is faster than splitting an PRNGKey because it allows generating new PRNG
  keys in parallel that are independent of each other.

  Args:
   rng: the rng to fold the string into.
   data: the string to be folded in.

  Returns:
   The newly generated PRNG key.
  """
  if not data:
    return rng
  m = hashlib.sha1()
  for x in data:
    if config.flax_fix_rng_separator:
      # encode seperate to avoid collisions like for example: ("ab", "c") and ("a", "bc")
      m.update(b'\00')
    if isinstance(x, str):
      m.update(x.encode('utf-8'))
    elif isinstance(x, int):
      m.update(x.to_bytes((x.bit_length() + 7) // 8, byteorder='big'))
    else:
      raise ValueError(f'Expected int or string, got: {x}')
  d = m.digest()
  hash_int = int.from_bytes(d[:4], byteorder='big')
  return random.fold_in(rng, jnp.uint32(hash_int))  # type: ignore

