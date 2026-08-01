
def _promote_integer_dtype(dtype: DType) -> DType:
  # Note: NumPy always promotes to 64-bit; jax instead promotes to the
  # default dtype as defined by dtypes.int_ or dtypes.uint.
  if dtypes.issubdtype(dtype, np.bool_):
    return dtypes.default_int_dtype()
  elif dtypes.issubdtype(dtype, np.unsignedinteger):
    default_uint_dtype = dtypes.default_uint_dtype()
    if np.iinfo(dtype).bits < np.iinfo(default_uint_dtype).bits:
      return default_uint_dtype
  elif dtypes.issubdtype(dtype, np.integer):
    default_int_dtype = dtypes.default_int_dtype()
    if np.iinfo(dtype).bits < np.iinfo(default_int_dtype).bits:
      return default_int_dtype
  return dtype

