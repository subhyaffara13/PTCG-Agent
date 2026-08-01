
def _philox2x32_fold_in(key: typing.Array, data: typing.Array) -> typing.Array:
  """Internal implementation of philox2x32_fold_in."""
  out0, _ = philox2x32_p.bind(key[0], np.uint32(0), data)
  return jnp.array([out0], dtype=np.uint32)

