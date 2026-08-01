
def _qr_dtype_rule(dtype, *, pivoting, **_):
  return (dtype, dtype, dtypes.dtype(np.int32)) if pivoting else (dtype, dtype)

