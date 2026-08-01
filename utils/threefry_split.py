
def threefry_split(key: typing.Array, shape: prng.Shape) -> typing.Array:
  shape = tuple(map(core.concrete_dim_or_error, shape))
  return _threefry_split(key, shape)

