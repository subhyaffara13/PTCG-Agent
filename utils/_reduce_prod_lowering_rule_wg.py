
def _reduce_prod_lowering_rule_wg(ctx: LoweringRuleContext, x, *, axes):
  [x_aval] = ctx.avals_in
  if jnp.issubdtype(x_aval.dtype, jnp.floating):
    acc = 1.0
  elif jnp.issubdtype(x_aval.dtype, jnp.integer):
    acc = 1
  else:
    raise NotImplementedError(f"Unsupported dtype {x_aval.dtype}")
  kind = vector_dialect.CombiningKind.MUL
  return _reduce_lowering_rule_wg(ctx, kind, acc, x, axes)

