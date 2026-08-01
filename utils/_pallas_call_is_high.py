
def _pallas_call_is_high(*_, jaxpr, **params):
  del params
  return jaxpr.is_high

