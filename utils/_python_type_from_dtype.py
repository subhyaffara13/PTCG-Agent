
def _python_type_from_dtype(dtype):
  if hasattr(dtype, 'type'):
    return type(dtype.type(0).item())
  else:
    return type(dtype(0).item())

