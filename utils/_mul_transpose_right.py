
def _mul_transpose_right(ct, x, y, *, out_dtype):
  g = mul(x, ct, out_dtype=None if out_dtype is None else y.aval.dtype)
  return _unbroadcast(y.aval, g)

