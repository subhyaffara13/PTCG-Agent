
def default_complex_dtype() -> DType:
  return (
      np.dtype(np.complex128)
      if config.enable_x64.value
      else np.dtype(np.complex64)
  )

