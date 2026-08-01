
def to_floating_dtype(dtype: DTypeLike) -> DType:
  """Promotes a dtype to a non-complex floating dtype."""
  dtype_ = np.dtype(dtype)
  return finfo(_dtype_to_inexact.get(dtype_, dtype_)).dtype

