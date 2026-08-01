
def last_used(jaxpr: Jaxpr) -> dict[Var, JaxprEqn | None]:
  """Returns a mapping from every var in jaxpr to what equation uses it last."""
  last_used: dict[Var, JaxprEqn | None] = {
      v: None for v in jaxpr.outvars if not isinstance(v, Literal)}
  for eqn in reversed(jaxpr.eqns):
    for v in eqn.invars:
      if not isinstance(v, Literal) and v not in last_used:
        last_used[v] = eqn
  return last_used

