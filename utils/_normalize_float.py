
def _normalize_float(x):
  info = dtypes.finfo(dtypes.dtype(x))
  int_type = _INT_DTYPES[info.bits]
  cond = lax.abs(x) < info.tiny
  x1 = _where(cond, x * _lax_const(x, 1 << info.nmant), x)
  x2 = _where(cond, int_type(-info.nmant), int_type(0))
  return lax.bitcast_convert_type(x1, int_type), x2

