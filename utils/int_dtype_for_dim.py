
def int_dtype_for_dim(d: DimSize, *, signed: bool) -> DType:
  """Returns a integer dtype large enough to contain indices in dimension d."""
  if signed:
    if not core.is_constant_dim(d):
      return dtypes.default_int_dtype()
    return np.dtype(np.int64) if d > _int32_max else np.dtype(np.int32)
  else:
    if not core.is_constant_dim(d):
      return dtypes.default_uint_dtype()
    return np.dtype(np.uint64) if d > _uint32_max else np.dtype(np.uint32)

