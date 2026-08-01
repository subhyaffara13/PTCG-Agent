
def _run_scoped_is_high(*avals, jaxpr, **params):
  del avals, params
  return jaxpr.is_high

