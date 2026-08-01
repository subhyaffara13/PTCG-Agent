
def threefry4x32_split(key: typing.Array, shape: prng.Shape) -> typing.Array:
  """Split a Threefry 4x32 key into multiple sub-keys.

  Args:
    key: A 4-word uint32 PRNG key with shape (4,).
    shape: The shape of the output array of sub-keys.

  Returns:
    A batched array of sub-keys with shape (*shape, 4).
  """
  shape = tuple(map(core.concrete_dim_or_error, shape))
  return _threefry4x32_split(key, shape)

