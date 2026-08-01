
def _is_threefry4x32_key(key: typing.Array) -> bool:
  """Check if the key is a valid Threefry 4x32 PRNG key."""
  try:
    return key.shape == (4,) and key.dtype == np.uint32
  except AttributeError:
    return False

