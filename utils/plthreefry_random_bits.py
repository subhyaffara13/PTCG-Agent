
def plthreefry_random_bits(key, bit_width: int, shape: Shape):
  if bit_width != 32:
    raise ValueError("Only 32-bit PRNG supported.")
  if len(shape) == 0:
    return plthreefry_random_bits(key, bit_width, (1, 1))[0, 0]
  elif len(shape) == 1:
    return plthreefry_random_bits(key, bit_width, (1, *shape))[0]

  requires_pad = (
      shape[-2] % BLOCK_SIZE[-2] != 0) or (shape[-1] % BLOCK_SIZE[-1] != 0)
  if requires_pad:
    padded_shape = tuple(shape[:-2]) + (
        prng_utils.round_up(shape[-2], BLOCK_SIZE[-2]),
        prng_utils.round_up(shape[-1], BLOCK_SIZE[-1]),
    )
    padded_result = threefry_2x32_count(
        key, padded_shape, shape, block_size=BLOCK_SIZE)
    return padded_result[..., :shape[-2], :shape[-1]]
  else:
    return threefry_2x32_count(key, shape, shape, block_size=BLOCK_SIZE)

