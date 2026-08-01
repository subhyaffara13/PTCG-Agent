
def _normalize_tolerance(tol: int | float | ToleranceDict | None) -> ToleranceDict:
  tol = tol or 0
  if isinstance(tol, dict):
    return {np.dtype(k): v for k, v in tol.items()}
  else:
    return dict.fromkeys(_default_tolerance, tol)

