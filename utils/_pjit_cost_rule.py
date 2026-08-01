
def _pjit_cost_rule(ctx, *, jaxpr: jax_core.ClosedJaxpr, **_):
  del ctx
  inner_cost = cost_estimate_jaxpr(jaxpr)
  return CostEstimate(
      flops=inner_cost.flops,
      transcendentals=inner_cost.transcendentals,
      bytes_accessed=inner_cost.bytes_accessed,
  )

