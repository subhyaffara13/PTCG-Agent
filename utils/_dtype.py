
def _dtype(x):
  try:
    return dtypes.result_type(x)
  except ValueError:
    return dtypes.result_type(getattr(x, 'dtype'))


def _dtype(x: Any) -> np.dtype:
  if hasattr(x, 'dtype'):
    return x.dtype
  elif (dt := _dtypes.python_scalar_types_to_dtypes.get(type(x))) is not None:
    return dt
  else:
    return np.asarray(x).dtype

