
def _downcast_to_small_type(array: np.ndarray) -> np.ndarray:
  """Downcast numpy array.

  If possible, downcast the data-type of the input array to the smallest numpy
  type (among np.int16 and np.int8) that fits the content of the array.

  Args:
    array: the array to downcast

  Returns:
    The downcasted array.

  Raises:
    ValueError: if the input array is not np.int32 or if its elements are not
    all positive.
  """

  if array.dtype != np.int32:
    raise ValueError('Expected int32 input.')

  if not np.all(array >= 0):
    raise ValueError('Expected non-negative array.')

  if array.size == 0:
    return array

  max_value = np.max(array)

  if max_value <= np.iinfo(np.int8).max:
    return array.astype(np.int8)
  elif max_value <= np.iinfo(np.int16).max:
    return array.astype(np.int16)
  else:
    return array.astype(np.int32)

