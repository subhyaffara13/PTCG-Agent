
def _is_threefry_prng_key(key: typing.Array) -> bool:
  try:
    return key.shape == (2,) and key.dtype == np.uint32
  except AttributeError:
    return False

