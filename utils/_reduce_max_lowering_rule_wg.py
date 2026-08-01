
def _reduce_max_lowering_rule_wg(ctx: LoweringRuleContext, x, *, axes):
  [x_aval] = ctx.avals_in
  if jnp.issubdtype(x_aval.dtype, jnp.floating):
    kind = vector_dialect.CombiningKind.MAXIMUMF
    acc = float("-inf")
  elif jnp.issubdtype(x_aval.dtype, jnp.integer):
    if jnp.issubdtype(x_aval.dtype, jnp.signedinteger):
      kind = vector_dialect.CombiningKind.MAXSI
    else:
      kind = vector_dialect.CombiningKind.MAXUI
    acc = np.iinfo(x_aval.dtype).min
  else:
    raise NotImplementedError(f"Unsupported dtype {x_aval.dtype}")
  return _reduce_lowering_rule_wg(ctx, kind, acc, x, axes)

