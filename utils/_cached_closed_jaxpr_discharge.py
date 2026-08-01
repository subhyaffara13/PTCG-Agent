
def _cached_closed_jaxpr_discharge(closed_jaxpr: core.ClosedJaxpr):
  num_outs = len(closed_jaxpr.outvars)
  discharged_closed_jaxpr = discharge_state(closed_jaxpr)
  fun = lu.wrap_init(core.jaxpr_as_fun(discharged_closed_jaxpr),
                     debug_info=discharged_closed_jaxpr.debug_info)
  return discharged_closed_jaxpr, num_outs, fun

