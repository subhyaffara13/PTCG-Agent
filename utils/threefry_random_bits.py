
def threefry_random_bits(key: typing.Array, bit_width, shape):
  """Sample uniform random bits of given width and shape using PRNG key."""
  if not _is_threefry_prng_key(key):
    raise TypeError("threefry_random_bits got invalid prng key.")
  if bit_width not in (8, 16, 32, 64):
    raise TypeError("requires 8-, 16-, 32- or 64-bit field width.")

  if config.threefry_partitionable.value:
    return _threefry_random_bits_partitionable(key, bit_width, shape)
  else:
    return _threefry_random_bits_original(key, bit_width, shape)

