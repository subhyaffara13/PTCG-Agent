
def _multiple_of_lane_lowering_rule(ctx: LoweringRuleContext, val, *, values):
  del ctx, values
  # Under Lane lowering semantics, we currently don't do anything with the
  # annotation.
  return val

