
def _rbg_random_bits(key: typing.Array, bit_width: int, shape: Sequence[int]
                     ) -> typing.Array:
  if not key.shape == (4,) and key.dtype == np.dtype('uint32'):
    raise TypeError("_rbg_random_bits got invalid prng key.")
  if bit_width not in (8, 16, 32, 64):
    raise TypeError("requires 8-, 16-, 32- or 64-bit field width.")
  _, bits = lax.rng_bit_generator(key, shape, dtype=prng.UINT_DTYPES[bit_width])
  return bits

