
def dtype_to_string(dtype):
  try:
    return str(np.dtype(dtype).name)
  except TypeError:
    pass
  try:
    return dtype.name
  except AttributeError:
    pass
  return str(dtype)

