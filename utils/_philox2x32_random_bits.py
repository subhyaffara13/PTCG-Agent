
def _philox2x32_random_bits(
    key: typing.Array, bit_width: int, shape: tuple[int, ...]
) -> typing.Array:
  """Internal implementation of philox2x32_random_bits."""
  if all(core.is_constant_dim(d) for d in shape) and math.prod(shape) > 2**64:
    raise NotImplementedError("random bits array of size exceeding 2 ** 64")

  counts1, counts2 = prng.iota_2x32_shape(shape)
  out0, out1 = philox2x32_p.bind(key[0], counts1, counts2)

  dtype = prng.UINT_DTYPES[bit_width]
  if bit_width == 64:
    bits_hi = lax.convert_element_type(out0, dtype)
    bits_lo = lax.convert_element_type(out1, dtype)
    return lax.shift_left(bits_hi, jnp.asarray(32, dtype=dtype)) | bits_lo
  elif bit_width == 32:
    return out0 ^ out1
  else:
    return lax.convert_element_type(out0 ^ out1, dtype)

