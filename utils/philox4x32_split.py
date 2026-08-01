
def philox4x32_split(key: typing.Array, shape: prng.Shape) -> typing.Array:
  """Split a Philox 4x32 key into multiple sub-keys."""
  shape = tuple(map(core.concrete_dim_or_error, shape))
  return _philox4x32_split(key, shape)

