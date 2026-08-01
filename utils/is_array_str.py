
def is_array_str(x: Any) -> bool:
  """Returns True if the given array is a `str` array.

  Note: Also returns True for scalar `str`, `bytes` values. For compatibility
  with `tensor.numpy()` which returns `bytes`

  Args:
    x: The array to test

  Returns:
    True or False
  """
  # `Tensor(shape=(), dtype=tf.string).numpy()` returns `bytes`.
  if isinstance(x, (bytes, str)):
    return True
  elif is_array(x):
    return is_dtype_str(x.dtype)
  else:
    return False

