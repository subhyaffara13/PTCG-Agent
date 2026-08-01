
def to_inexact_dtype(dtype: DTypeLike) -> DType:
  """Promotes a dtype into an inexact dtype, if it is not already one."""
  dtype_ = np.dtype(dtype)
  return _dtype_to_inexact.get(dtype_, dtype_)

