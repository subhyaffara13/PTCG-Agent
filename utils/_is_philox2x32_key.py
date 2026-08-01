
def _is_philox2x32_key(key: typing.Array) -> bool:
  """Return True if the input is a valid Philox 2x32 PRNG key."""
  try:
    return key.shape == (1,) and key.dtype == np.uint32
  except AttributeError:
    return False

