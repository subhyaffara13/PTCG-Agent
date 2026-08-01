
def _philox2x32_split(key: typing.Array, shape: prng.Shape) -> typing.Array:
  """Internal implementation of philox2x32_split."""
  counts1, counts2 = prng.iota_2x32_shape(shape)
  out0, _ = philox2x32_p.bind(key[0], counts1, counts2)
  return lax.expand_dims(out0, [len(shape)])

