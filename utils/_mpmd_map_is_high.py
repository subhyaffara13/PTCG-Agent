
def _mpmd_map_is_high(*args, jaxprs, **params):
  del args, params
  return any(jaxpr.is_high for jaxpr in jaxprs)

