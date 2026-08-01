
def _philox4x32_split(key: typing.Array, shape: prng.Shape) -> typing.Array:
  """Internal implementation of philox4x32_split."""
  k0, k1 = key[0], key[1]

  # Generate counters for each sub-key.
  counts1, counts2 = prng.iota_2x32_shape(shape)
  zeros = jnp.zeros(shape, dtype=np.uint32)

  out0, out1, _, _ = philox4x32_p.bind(k0, k1, zeros, zeros, counts1, counts2)

  return jnp.stack([out0, out1], axis=len(shape))

