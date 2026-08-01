
def _abs_lowering_rule_wg(ctx: LoweringRuleContext, x):
  [x_aval] = ctx.avals_in
  x = _ensure_ir_value(x, x_aval.dtype)
  if jnp.issubdtype(x_aval.dtype, jnp.floating):
    return math_dialect.absf(x)
  if jnp.issubdtype(x_aval.dtype, jnp.integer):
    return math_dialect.absi(x)
  raise NotImplementedError(f"Unsupported dtype for abs: {x_aval.dtype}")

