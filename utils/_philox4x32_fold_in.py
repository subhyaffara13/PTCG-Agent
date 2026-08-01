
def _philox4x32_fold_in(key: typing.Array, data: typing.Array) -> typing.Array:
  """Internal implementation of philox4x32_fold_in."""
  # Hash the key with the data used as part of the counter.
  k0, k1 = key[0], key[1]
  out0, out1, _, _ = philox4x32_p.bind(
      k0, k1, np.uint32(0), np.uint32(0), np.uint32(0), data
  )
  return jnp.array([out0, out1], dtype=np.uint32)

