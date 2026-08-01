
def _supported_dtype(dtype: np.dtype | None):
  return dtype is not None and (
      dtype_util.is_integer_dtype(dtype)
      or dtype_util.is_floating_dtype(dtype)
      or np.issubdtype(dtype, np.bool_)
  )

