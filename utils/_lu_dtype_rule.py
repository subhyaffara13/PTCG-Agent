
def _lu_dtype_rule(dtype, **_):
  return dtype, dtypes.dtype(np.int32), dtypes.dtype(np.int32)

