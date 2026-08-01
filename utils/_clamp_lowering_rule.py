
def _clamp_lowering_rule(ctx: LoweringRuleContext, min, operand, max):
  """Compute minimum_p(maximum_p(min, operand), max)."""
  return lower_fun(_clamp)(ctx, min, operand, max)


def _clamp_lowering_rule(ctx: LoweringRuleContext, l, x, u):
  return _lower_fun(lambda l, x, u: lax.min(lax.max(x, l), u))(ctx, l, x, u)

