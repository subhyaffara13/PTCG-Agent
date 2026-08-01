
def philox4x32_fold_in(key: typing.Array, data: typing.Array) -> typing.Array:
  """Fold-in an integer value to create a new Philox4x32 key."""
  assert not data.shape
  return _philox4x32_fold_in(key, jnp.asarray(data, dtype="uint32"))

