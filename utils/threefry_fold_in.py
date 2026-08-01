
def threefry_fold_in(key: typing.Array, data: typing.Array) -> typing.Array:
  assert not data.shape
  return _threefry_fold_in(key, jnp.asarray(data, dtype='uint32'))

