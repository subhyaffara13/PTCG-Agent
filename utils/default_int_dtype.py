
def default_int_dtype() -> DType:
  return np.dtype(np.int64) if config.enable_x64.value else np.dtype(np.int32)

