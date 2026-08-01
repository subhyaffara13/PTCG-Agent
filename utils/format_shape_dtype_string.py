
def format_shape_dtype_string(shape, dtype):
  if isinstance(shape, np.ndarray):
    return f'{dtype_str(dtype)}[{shape}]'
  elif isinstance(shape, list):
    shape = tuple(shape)
  return _format_shape_dtype_string(shape, dtype)

