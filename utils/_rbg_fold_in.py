
def _rbg_fold_in(key: typing.Array, data: typing.Array) -> typing.Array:
  assert not data.shape
  return api.vmap(threefry2x32._threefry_fold_in, (0, None), 0)(key.reshape(2, 2), data).reshape(4)

