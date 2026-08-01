
def _core_map_rule(ctx: Context, *args, jaxpr, **params):
  _assert_no_fusion_types(ctx.avals_in)
  _assert_no_fusion_types(ctx.avals_out)
  assert not jaxpr.invars
  with core.extend_axis_env_nd(params["mesh"].shape.items()):
    jaxpr = physicalize_jaxpr(jaxpr)
  return pallas_core.core_map_p.bind(*args, jaxpr=jaxpr, **params)

