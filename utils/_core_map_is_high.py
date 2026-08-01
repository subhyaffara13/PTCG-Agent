
def _core_map_is_high(*avals, jaxpr, **params):
  del avals, params
  return jaxpr.is_high

