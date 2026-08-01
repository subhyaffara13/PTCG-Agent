
def _empty_ref_lowering_rule(ctx: LoweringRuleContext, ty, memory_space):
  del ty, memory_space
  [aval_out] = ctx.avals_out
  return _alloc_value(aval_out, ctx=ctx)


def _empty_ref_lowering_rule(ctx: LoweringRuleContext, ty, memory_space):
  del ty, memory_space
  [aval_out] = ctx.avals_out
  return tc_lowering._alloc_value(aval_out, ctx=ctx)

