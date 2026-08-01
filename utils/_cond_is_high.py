
def _cond_is_high(*_, branches, **__) -> bool:
  return any(j.jaxpr.is_high for j in branches)

