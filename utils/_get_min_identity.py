
def _get_min_identity(dt):
  return np.inf if dtypes.issubdtype(dt, np.floating) else np.iinfo(dt).max


def _get_min_identity(dtype):
  if dtypes.issubdtype(dtype, np.inexact):
    return np.array(np.inf, dtype)
  elif dtypes.issubdtype(dtype, np.integer):
    return np.array(dtypes.iinfo(dtype).max, dtype)
  elif dtypes.issubdtype(dtype, np.bool_):
    return np.array(True, np.bool_)


def _get_min_identity(dtype: DTypeLike) -> np.ndarray:
  if dtypes.issubdtype(dtype, np.inexact):
    return np.array(np.inf if dtypes.supports_inf(dtype) else dtypes.finfo(dtype).max,
                    dtype=dtype)
  elif dtypes.issubdtype(dtype, np.integer):
    return np.array(dtypes.iinfo(dtype).max, dtype)
  elif dtypes.issubdtype(dtype, np.bool_):
    return np.array(True, np.bool_)
  else:
    raise ValueError(f"Unsupported dtype for min: {dtype}")

