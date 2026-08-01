
def _close_jaxpr(jaxpr: core.Jaxpr) -> core.ClosedJaxpr:
  return pe.close_jaxpr(pe.convert_constvars_jaxpr(jaxpr))

