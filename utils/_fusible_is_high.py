
def _fusible_is_high(*_, jaxpr, **params):
  del params
  return jaxpr.is_high

