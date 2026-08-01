
def _np_dtype_to_python_type(dtype):
  """Converts dtype by checking its fundamental type."""
  if np.issubdtype(dtype, np.integer):
    return int
  elif np.issubdtype(dtype, np.floating):
    return float
  else:
    raise TypeError(f"Unsupported dtype: {dtype}.")

