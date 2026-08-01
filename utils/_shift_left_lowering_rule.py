
def _shift_left_lowering_rule(ctx: LoweringRuleContext, x, d):
  x, d = _bcast(
      x,
      d,
      ctx.avals_in[0],
      ctx.avals_in[1],
      ctx.avals_out[0],
      ctx.lowering_context.dynamic_shape_replacement_fn,
  )
  return arith.shli(x, d)

