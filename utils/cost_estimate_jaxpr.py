
def cost_estimate_jaxpr(
    jaxpr: jax_core.ClosedJaxpr,
) -> pallas_core.CostEstimate:
  """Returns the cost estimate for the given Jaxpr."""
  jaxpr, _ = jaxpr.jaxpr, jaxpr.consts
  total_cost = CostEstimate(flops=0, transcendentals=0, bytes_accessed=0)

  for eqn in jaxpr.eqns:
    rule = _cost_rules.get(eqn.primitive, None)
    if rule is not None:
      context = Context(avals_in=[v.aval for v in eqn.invars],
                        avals_out=[v.aval for v in eqn.outvars])
      op_cost = rule(context, **eqn.params)
      total_cost = total_cost + op_cost
  return pallas_core.CostEstimate(
      flops=total_cost.flops,
      transcendentals=total_cost.transcendentals,
      bytes_accessed=total_cost.bytes_accessed,
  )

