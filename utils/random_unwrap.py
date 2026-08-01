
def random_unwrap(keys):
  if not dtypes.issubdtype(keys.dtype, dtypes.prng_key):
    raise TypeError(f'random_unwrap takes key array operand, got {keys.dtype=}')
  return random_unwrap_p.bind(keys)

