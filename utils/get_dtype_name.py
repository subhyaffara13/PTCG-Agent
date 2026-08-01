
def get_dtype_name(dtype: numpy.typing.DTypeLike) -> str:
  """Safely extracts a name for a dtype."""
  # Render scalar type objects as their literal names.
  if isinstance(dtype, type) and issubclass(dtype, np.generic):
    return dtype.__name__
  # Render any other dtype-like objects as the name of the concrete dtype they
  # convert to.
  try:
    return np.dtype(dtype).name
  except TypeError:
    return str(dtype)

