
def _threefry_random_bits_partitionable(key: typing.Array, bit_width, shape):
  if all(core.is_constant_dim(d) for d in shape) and math.prod(shape) > 2 ** 64:
    raise NotImplementedError('random bits array of size exceeding 2 ** 64')

  k1, k2 = key
  counts1, counts2 = prng.iota_2x32_shape(shape)
  bits1, bits2 = threefry2x32_p.bind(k1, k2, counts1, counts2)

  dtype = prng.UINT_DTYPES[bit_width]
  if bit_width == 64:
    bits_hi = lax.convert_element_type(bits1, dtype)
    bits_lo = lax.convert_element_type(bits2, dtype)
    return lax.shift_left(bits_hi, jnp.asarray(32, dtype=dtype)) | bits_lo
  elif bit_width == 32:
    return bits1 ^ bits2
  else:
    return lax.convert_element_type(bits1 ^ bits2, dtype)

