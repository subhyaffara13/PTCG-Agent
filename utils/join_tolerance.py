
def join_tolerance(
    tol1: int | float | ToleranceDict | None,
    tol2: int | float | ToleranceDict | None) -> ToleranceDict:
  tol1 = _normalize_tolerance(tol1)
  tol2 = _normalize_tolerance(tol2)
  out = tol1
  for k, v in tol2.items():
    out[k] = max(v, tol1.get(k, 0))
  return out

