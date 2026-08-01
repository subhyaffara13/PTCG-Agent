
def _mul_transpose_left(ct, x, y, *, out_dtype):
  g = mul(ct, y, out_dtype=None if out_dtype is None else x.aval.dtype)
  return _unbroadcast(x.aval, g)

