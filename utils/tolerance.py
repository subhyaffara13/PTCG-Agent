
def tolerance(dtype: np.dtype, tol: int | float | ToleranceDict | None = None) -> int | float:
  tol = {} if tol is None else tol
  if not isinstance(tol, dict):
    return tol
  tol = {np.dtype(key): value for key, value in tol.items()}
  dtype = _dtypes.canonicalize_dtype(np.dtype(dtype))
  return tol.get(dtype, default_tolerance()[dtype])

