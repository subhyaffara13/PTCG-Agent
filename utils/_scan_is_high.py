
def _scan_is_high(*_, jaxpr, **__) -> bool:
  return jaxpr.jaxpr.is_high

