
def to_numeric_dtype(dtype: DTypeLike) -> DType:
  """Promotes a dtype into an numeric dtype, if it is not already one."""
  dtype_ = np.dtype(dtype)
  return np.dtype('int32') if dtype_ == np.dtype('bool') else dtype_

