
def separate_consts(jaxpr: ClosedJaxpr) -> tuple[ClosedJaxpr, list[Any]]:
  """Moves the constvars to the start of invars and returns the consts explicitly."""
  return close_jaxpr(convert_constvars_jaxpr(jaxpr.jaxpr)), jaxpr.consts

