
def _scan_rule(ctx: Context, *args, jaxpr, **params):
  _assert_no_fusion_types(ctx.avals_in)
  _assert_no_fusion_types(ctx.avals_out)
  jaxpr = physicalize_closed_jaxpr(jaxpr)
  return jax.lax.scan_p.bind(*args, jaxpr=jaxpr, **params)

