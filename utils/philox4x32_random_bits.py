
def philox4x32_random_bits(
    key: typing.Array, bit_width: int, shape: tuple[int, ...]
) -> typing.Array:
  """Sample uniform random bits using a Philox 4x32 key."""
  if not _is_philox4x32_key(key):
    raise TypeError("philox4x32_random_bits got invalid prng key.")
  if bit_width not in (8, 16, 32, 64):
    raise TypeError("requires 8-, 16-, 32- or 64-bit field width.")
  return _philox4x32_random_bits(key, bit_width, shape)

