import math


def _threefry4x32_random_bits(
    key: typing.Array, bit_width: int, shape: tuple[int, ...]
) -> typing.Array:
  """Sample uniform random bits using a Threefry 4x32 key."""
  if all(core.is_constant_dim(d) for d in shape) and math.prod(shape) > 2**64:
    raise NotImplementedError("random bits array of size exceeding 2 ** 64")

  k0, k1, k2, k3 = key[0], key[1], key[2], key[3]
  counts1, counts2 = prng.iota_2x32_shape(shape)
  zeros = jnp.zeros(shape, dtype=np.uint32)

  out0, out1, out2, out3 = threefry4x32_p.bind(
      k0, k1, k2, k3, counts1, counts2, zeros, zeros
  )

  dtype = prng.UINT_DTYPES[bit_width]
  if bit_width == 64:
    # Combine four 32-bit outputs into one 64-bit value.
    bits_hi = lax.convert_element_type(out0 ^ out2, dtype)
    bits_lo = lax.convert_element_type(out1 ^ out3, dtype)
    return lax.shift_left(bits_hi, jnp.asarray(32, dtype=dtype)) | bits_lo
  elif bit_width == 32:
    # XOR all four outputs for maximum mixing.
    return out0 ^ out1 ^ out2 ^ out3
  else:
    return lax.convert_element_type(out0 ^ out1 ^ out2 ^ out3, dtype)

