
def philox2x32_fold_in(key: typing.Array, data: typing.Array) -> typing.Array:
  """Fold-in an integer value to create a new Philox2x32 key."""
  assert not data.shape
  return _philox2x32_fold_in(key, jnp.asarray(data, dtype="uint32"))

