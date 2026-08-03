import math


def _philox4x32_random_bits(
    key: typing.Array, bit_width: int, shape: tuple[int, ...]
) -> typing.Array:
  """Internal implementation of philox4x32_random_bits."""
  if all(core.is_constant_dim(d) for d in shape) and math.prod(shape) > 2**64:
    raise NotImplementedError("random bits array of size exceeding 2 ** 64")

  k0, k1 = key[0], key[1]
  counts1, counts2 = prng.iota_2x32_shape(shape)
  zeros = jnp.zeros(shape, dtype=np.uint32)

  out0, out1, out2, out3 = philox4x32_p.bind(
      k0, k1, counts1, counts2, zeros, zeros
  )

  dtype = prng.UINT_DTYPES[bit_width]
  if bit_width == 64:
    # Combine two 32-bit outputs into one 64-bit value.
    bits_hi = lax.convert_element_type(out0, dtype)
    bits_lo = lax.convert_element_type(out1, dtype)
    return lax.shift_left(bits_hi, jnp.asarray(32, dtype=dtype)) | bits_lo
  elif bit_width == 32:
    # XOR all four outputs for maximum mixing.
    return out0 ^ out1 ^ out2 ^ out3
  else:
    return lax.convert_element_type(out0 ^ out1 ^ out2 ^ out3, dtype)

