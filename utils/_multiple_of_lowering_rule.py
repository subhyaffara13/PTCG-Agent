
def _multiple_of_lowering_rule(ctx: LoweringRuleContext, val, *, values):
  del ctx
  for multiple in values:
    val = tpu.assume_multiple(val, multiple)
  return val

