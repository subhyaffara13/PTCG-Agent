
def _rbg_split(key: typing.Array, shape: prng.Shape) -> typing.Array:
  if config.threefry_partitionable.value:
    _threefry_split = threefry2x32._threefry_split_foldlike
  else:
    _threefry_split = threefry2x32._threefry_split_original
  halfkeys = key.reshape(2, 2)
  return api.vmap(
      _threefry_split, (0, None), len(shape))(halfkeys, shape).reshape(
          *shape, 4)

