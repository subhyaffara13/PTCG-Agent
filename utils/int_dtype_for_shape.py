
def int_dtype_for_shape(shape: Shape, *, signed: bool) -> DType:
  """Returns a integer dtype large enough to contain indices in `shape`."""
  if signed:
    for d in shape:
      if core.is_constant_dim(d):
        if d > _int32_max:
          return np.dtype(np.int64)
      else:
        return dtypes.default_int_dtype()
    return np.dtype(np.int32)
  else:
    for d in shape:
      if core.is_constant_dim(d):
        if d > _uint32_max:
          return np.dtype(np.uint64)
      else:
        return dtypes.default_uint_dtype()
    return np.dtype(np.uint32)

