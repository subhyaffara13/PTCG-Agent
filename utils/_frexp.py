
def _frexp(x):
  dtype = dtypes.dtype(x)
  info = dtypes.finfo(dtype)
  mask = (1 << info.nexp) - 1
  bias = 1 - info.minexp

  x1, x2 = _normalize_float(x)
  x2 += ((x1 >> info.nmant) & mask) - bias + 1
  x1 &= ~(mask << info.nmant)
  x1 |= (bias - 1) << info.nmant
  x1 = lax.bitcast_convert_type(x1, dtype)

  cond = isinf(x) | isnan(x) | (x == 0)
  x2 = _where(cond, lax._zeros(x2), x2)
  return _where(cond, x, x1), lax.convert_element_type(x2, np.int32)

