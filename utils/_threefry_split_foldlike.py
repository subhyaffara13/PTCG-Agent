
def _threefry_split_foldlike(key, shape) -> typing.Array:
  k1, k2 = key
  counts1, counts2 = prng.iota_2x32_shape(shape)
  bits1, bits2 = threefry2x32_p.bind(k1, k2, counts1, counts2)
  return jnp.stack([bits1, bits2], axis=bits1.ndim)

