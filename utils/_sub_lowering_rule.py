
def _sub_lowering_rule(ctx: LoweringRuleContext, x, y):
  x, y = _bcast(
      x,
      y,
      ctx.avals_in[0],
      ctx.avals_in[1],
      ctx.avals_out[0],
      ctx.lowering_context.dynamic_shape_replacement_fn,
  )
  (aval_out,) = ctx.avals_out
  if jnp.issubdtype(aval_out.dtype, jnp.integer):
    return arith.subi(x, y)
  if jnp.issubdtype(aval_out.dtype, jnp.floating):
    return arith.subf(x, y)
  raise NotImplementedError(aval_out.dtype)

