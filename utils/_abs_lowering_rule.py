
def _abs_lowering_rule(ctx: LoweringRuleContext, x):
  (aval_out,) = ctx.avals_out
  if jnp.issubdtype(aval_out.dtype, jnp.integer):
    return mlir_math.absi(x)
  if jnp.issubdtype(aval_out.dtype, jnp.floating):
    return mlir_math.absf(x)
  raise NotImplementedError(aval_out.dtype)


def _abs_lowering_rule(ctx: LoweringRuleContext, x):
  [x_aval] = ctx.avals_in
  return _ensure_fa(x, x_aval.dtype).abs()

