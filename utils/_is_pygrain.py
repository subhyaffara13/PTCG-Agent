
def _is_pygrain(array: Array) -> bool:
  if (
      'grain._src.python' not in sys.modules
      and 'grain.python' not in sys.modules
  ):
    return False

  return isinstance(array, _get_grain_shm_array_metadata_cls())

