
def _custom_vjp_rule(ctx, *, call_jaxpr: jax_core.ClosedJaxpr, **_):
  del ctx
  inner_cost = cost_estimate_jaxpr(call_jaxpr)
  return CostEstimate(
      flops=inner_cost.flops,
      transcendentals=inner_cost.transcendentals,
      bytes_accessed=inner_cost.bytes_accessed,
  )

