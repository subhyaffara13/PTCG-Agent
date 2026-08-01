
def _threefry4x32_fold_in(key: typing.Array, data: typing.Array) -> typing.Array:
  """Fold data into a Threefry 4x32 key."""
  # Hash the key with the data used as part of the counter.
  k0, k1, k2, k3 = key[0], key[1], key[2], key[3]
  out0, out1, out2, out3 = threefry4x32_p.bind(
      k0, k1, k2, k3, np.uint32(0), np.uint32(0), np.uint32(0), data
  )
  return jnp.array([out0, out1, out2, out3], dtype=np.uint32)

