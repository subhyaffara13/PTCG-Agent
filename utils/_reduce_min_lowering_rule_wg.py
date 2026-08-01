
def _reduce_min_lowering_rule_wg(ctx: LoweringRuleContext, x, *, axes):
  [x_aval] = ctx.avals_in
  if jnp.issubdtype(x_aval.dtype, jnp.floating):
    kind = vector_dialect.CombiningKind.MINIMUMF
    acc = float("inf")
  elif jnp.issubdtype(x_aval.dtype, jnp.integer):
    if jnp.issubdtype(x_aval.dtype, jnp.signedinteger):
      kind = vector_dialect.CombiningKind.MINSI
    else:
      kind = vector_dialect.CombiningKind.MINUI
    acc = np.iinfo(x_aval.dtype).max
  else:
    raise NotImplementedError(f"Unsupported dtype {x_aval.dtype}")
  return _reduce_lowering_rule_wg(ctx, kind, acc, x, axes)

