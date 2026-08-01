
def _is_philox4x32_key(key: typing.Array) -> bool:
  """Return True if key is a Philox 4x32 key."""
  try:
    return key.shape == (2,) and key.dtype == np.uint32
  except AttributeError:
    return False

