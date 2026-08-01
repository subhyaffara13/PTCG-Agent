
def philox_random_bits(key, bit_width: int, shape: Shape):
  if bit_width != 32:
    raise ValueError("Only 32-bit PRNG supported.")
  return philox_4x32_count(key, shape, fuse_output=True)

