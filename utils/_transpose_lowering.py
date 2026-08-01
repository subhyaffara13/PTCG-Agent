
def _transpose_lowering(ctx: LoweringRuleContext, x, *, permutation):
  return tt_dialect.trans(x, permutation)

