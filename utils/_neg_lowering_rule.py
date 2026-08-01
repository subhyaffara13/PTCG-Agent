
def _neg_lowering_rule(ctx: LoweringRuleContext, x):
  (x_aval,) = ctx.avals_in
  new_ctx = ctx.replace(
      avals_in=(jax_core.ShapedArray((), x_aval.dtype), x_aval),
      block_shapes=((), *ctx.block_shapes)
  )
  return _sub_lowering_rule(new_ctx, np.array(0, dtype=x_aval.dtype), x)

