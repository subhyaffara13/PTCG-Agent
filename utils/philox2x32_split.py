
def philox2x32_split(key: typing.Array, shape: prng.Shape) -> typing.Array:
  """Split a Philox 2x32 PRNG key into multiple sub-keys."""
  shape = tuple(map(core.concrete_dim_or_error, shape))
  return _philox2x32_split(key, shape)

