
def _convert_to_array_if_dtype_fails(x: ArrayLike) -> ArrayLike:
  try:
    dtypes.dtype(x)
  except TypeError:
    return np.asarray(x)
  else:
    return x

