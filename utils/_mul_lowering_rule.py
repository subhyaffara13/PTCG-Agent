
def _mul_lowering_rule(ctx: LoweringRuleContext, x, y, *, out_dtype):
  x, y = _bcast(
      x,
      y,
      ctx.avals_in[0],
      ctx.avals_in[1],
      ctx.avals_out[0],
      ctx.lowering_context.dynamic_shape_replacement_fn,
  )
  if out_dtype is not None:
    convert_to_out_dtype = lower_fun(lambda x: x.astype(out_dtype))
    x = convert_to_out_dtype(ctx, x)
    y = convert_to_out_dtype(ctx, y)
  (aval_out,) = ctx.avals_out
  if jnp.issubdtype(aval_out.dtype, jnp.integer):
    return arith.muli(x, y)
  if jnp.issubdtype(aval_out.dtype, jnp.floating):
    return arith.mulf(x, y)
  raise NotImplementedError(aval_out.dtype)

