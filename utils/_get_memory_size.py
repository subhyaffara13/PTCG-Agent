
def _get_memory_size(value: Any) -> int:
  """Gets memory size for a leaf value.

  The value is expected to be symmetric for save and load and represents the
  total memory allocated across all devices.

  Args:
    value: The leaf object to inspect.

  Returns:
    The estimated memory footprint in bytes.
  """
  if hasattr(value, 'nbytes'):
    return int(value.nbytes)
  if hasattr(value, 'shape') and hasattr(value, 'dtype'):
    itemsize = getattr(value.dtype, 'itemsize', 1)
    return int(math.prod(value.shape) * itemsize)
  if isinstance(value, (int, float, complex)):
    return sys.getsizeof(value)
  if isinstance(value, bytes):
    return len(value)
  if isinstance(value, str):
    return len(value.encode('utf-8'))
  return sys.getsizeof(value)

