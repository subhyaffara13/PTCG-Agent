
def threefry4x32_random_bits(
    key: typing.Array, bit_width: int, shape: tuple[int, ...]
) -> typing.Array:
  """Sample uniform random bits using a Threefry 4x32 key.

  Args:
    key: A 4-word uint32 PRNG key with shape (4,).
    bit_width: The bit width of the output random bits (8, 16, 32, or 64).
    shape: The shape of the output array of random bits.

  Returns:
    An array of uniform random bits with shape (*shape,) and dtype corresponding
    to the bit width.
  """
  if not _is_threefry4x32_key(key):
    raise TypeError("threefry4x32_random_bits got invalid prng key.")
  if bit_width not in (8, 16, 32, 64):
    raise TypeError("requires 8-, 16-, 32- or 64-bit field width.")
  return _threefry4x32_random_bits(key, bit_width, shape)

