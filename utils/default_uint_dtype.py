
def default_uint_dtype() -> DType:
  return np.dtype(np.uint64) if config.enable_x64.value else np.dtype(np.uint32)

