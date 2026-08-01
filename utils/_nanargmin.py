
def _nanargmin(a: Array, axis: int | None = None, keepdims : bool = False):
  if not issubdtype(a.dtype, np.inexact):
    return argmin(a, axis=axis, keepdims=keepdims)
  nan_mask = ufuncs.isnan(a)
  a = where(nan_mask, np.inf, a)
  res = argmin(a, axis=axis, keepdims=keepdims)
  return where(reductions.all(nan_mask, axis=axis, keepdims=keepdims), -1, res)

