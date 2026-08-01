
def _array_reduce_precision_handler(t, x):
  assert isinstance(t, core.ShapedArray)
  if dtypes.issubdtype(t.dtype, np.inexact):
    finfo = dtypes.finfo(t.dtype)
    return reduce_precision(x, exponent_bits=finfo.nexp, mantissa_bits=finfo.nmant)
  return x

