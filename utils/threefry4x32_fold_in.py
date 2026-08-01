
def threefry4x32_fold_in(key: typing.Array, data: typing.Array) -> typing.Array:
  """Fold data into a Threefry 4x32 key.

  Args:
    key: A 4-word uint32 PRNG key with shape (4,).
    data: A scalar integer array to fold into the key.

  Returns:
    A 4-word uint32 PRNG key with shape (*data.shape, 4,).
  """
  return _threefry4x32_fold_in(key, data)

