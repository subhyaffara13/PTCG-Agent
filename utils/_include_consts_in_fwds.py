
def _include_consts_in_fwds(consts, fwds, residuals):
  if all(f is None for f in fwds):
    return fwds, residuals
  dummys = [object() for _ in range(max(f for f in fwds if f is not None) + 1)]
  residuals_ = iter(residuals)
  residuals = [next(residuals_) if f is None else dummys[f] for f in fwds]
  assert next(residuals_, None) is None
  idxs = {id(x): i for i, x in enumerate((*consts, *dummys))}
  fwds = [idxs.get(id(r)) for r in residuals]
  residuals = [r for r in residuals if id(r) not in idxs]
  return fwds, residuals

