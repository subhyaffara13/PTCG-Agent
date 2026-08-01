
def _run_state_rule(*_, jaxpr: jax_core.Jaxpr, **_2):
  inner_cost = cost_estimate_jaxpr(pe.close_jaxpr(jaxpr))
  return CostEstimate(
      flops=inner_cost.flops,
      transcendentals=inner_cost.transcendentals,
      bytes_accessed=inner_cost.bytes_accessed,
  )


def _run_state_rule(ctx: Context, *args, jaxpr, which_linear, is_initialized):
  _assert_no_fusion_types(ctx.avals_in)
  _assert_no_fusion_types(ctx.avals_out)
  jaxpr = physicalize_jaxpr(jaxpr)
  return state_discharge.run_state_p.bind(
      *args,
      jaxpr=jaxpr,
      which_linear=which_linear,
      is_initialized=is_initialized,
  )

