
def _is_grain(array: Array) -> bool:
  if 'grain.tensorflow' not in sys.modules:
    return False
  from grain import tensorflow as grain  # pylint: disable=g-import-not-at-top  # pytype: disable=import-error

  return isinstance(array, grain.ArraySpec)

