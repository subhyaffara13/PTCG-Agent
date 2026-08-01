
def _cond_physicalize_rule(ctx: Context, *args, branches, **kwargs):
  _assert_no_fusion_types(ctx.avals_out)
  physicalized_branches = tuple(
      physicalize_closed_jaxpr(branch) for branch in branches
  )
  flat_args = jax.tree.leaves(args)
  return conditionals.cond_p.bind(
      *flat_args, branches=physicalized_branches, **kwargs
  )

