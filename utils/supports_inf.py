
def supports_inf(dtype: DTypeLike) -> bool:
  """Return true if the dtype supports infinity, else return False."""
  typ = np.dtype(dtype).type
  if typ in {float8_e4m3b11fnuz, float8_e4m3fn, float8_e4m3fnuz, float8_e5m2fnuz}:
    return False
  return issubdtype(dtype, np.inexact)

