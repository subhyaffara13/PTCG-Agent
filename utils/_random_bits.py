
def _random_bits(key: Array, bit_width: int, shape: Shape) -> Array:
  assert dtypes.issubdtype(key.dtype, dtypes.prng_key)
  return prng.random_bits(key, bit_width=bit_width, shape=shape)


def _random_bits(key: typing.Array, bit_width: int, shape: Shape):
  if bit_width != 32:
    raise ValueError("Bit width must be 32")
  prng_seed(key)
  return prng_random_bits(shape)

