
def _remat_is_high(*_, jaxpr, **__) -> bool:
  return jaxpr.is_high

