
def _pl_stateful_random_bits(key: typing.Array, bit_width: int, shape: Shape):
  del key
  assert bit_width == 32, "Bit width must be 32"
  return prng_random_bits(shape)

