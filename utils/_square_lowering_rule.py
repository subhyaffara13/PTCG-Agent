
def _square_lowering_rule(ctx: LoweringRuleContext, x):
  if jnp.issubdtype(ctx.avals_in[0].dtype, jnp.integer):
    return arith.muli(x, x)
  return arith.mulf(x, x)


def _square_lowering_rule(ctx: LoweringRuleContext, x):
  [x_aval] = ctx.avals_in
  if ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Lane:
    x = _ensure_fa(x, x_aval.dtype)
    return x * x
  if jnp.issubdtype(x_aval.dtype, jnp.integer):
    return arith_dialect.muli(x, x)
  if jnp.issubdtype(x_aval.dtype, jnp.floating):
    return arith_dialect.mulf(x, x)
  raise NotImplementedError(f"Unsupported dtype {x_aval.dtype}")

