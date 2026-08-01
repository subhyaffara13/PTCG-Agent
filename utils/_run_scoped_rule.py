
def _run_scoped_rule(ctx: Context, *args, jaxpr, **params):
  _assert_no_fusion_types(ctx.avals_out)
  jaxpr = physicalize_jaxpr(jaxpr)
  flat_args = tree_util.tree_leaves(args)
  assert len(flat_args) == len(
      jaxpr.constvars
  ), f"Length mismatch: {len(flat_args)=} != {len(jaxpr.constvars)=}"
  return pallas_primitives.run_scoped_p.bind(*flat_args, jaxpr=jaxpr, **params)

