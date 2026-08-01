
def dim_constant(ct: int):
  dtype = dim_value_dtype()
  assert dtype in (np.int32, np.int64)
  if dtype == np.int32:
    return np.int32(ct)
  elif dtype == np.int64:
    return np.int64(ct)

