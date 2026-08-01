
def _threefry4x32_split(key: typing.Array, shape: prng.Shape) -> typing.Array:
  """Split a Threefry 4x32 key into multiple sub-keys."""
  k0, k1, k2, k3 = key[0], key[1], key[2], key[3]

  # Generate counters for each sub-key.
  counts1, counts2 = prng.iota_2x32_shape(shape)
  zeros = jnp.zeros(shape, dtype=np.uint32)

  out0, out1, out2, out3 = threefry4x32_p.bind(
      k0, k1, k2, k3, zeros, zeros, counts1, counts2
  )

  return jnp.stack([out0, out1, out2, out3], axis=len(shape))

