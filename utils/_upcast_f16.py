
def _upcast_f16(dtype: DTypeLike) -> DType:
  if np.dtype(dtype) in [np.float16, dtypes.bfloat16]:
    return np.dtype('float32')
  return np.dtype(dtype)

