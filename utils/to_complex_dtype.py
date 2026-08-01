
def to_complex_dtype(dtype: DTypeLike) -> DType:
  ftype = to_inexact_dtype(dtype)
  if ftype in [np.dtype('float64'), np.dtype('complex128')]:
    return np.dtype('complex128')
  return np.dtype('complex64')

