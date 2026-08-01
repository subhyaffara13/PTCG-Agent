
def _reduce_sum_lowering_rule_wg(ctx: LoweringRuleContext, x, *, axes,
                                 out_sharding):
  kind = vector_dialect.CombiningKind.ADD
  return _reduce_lowering_rule_wg(ctx, kind, 0, x, axes)

