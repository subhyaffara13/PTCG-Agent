
def _broadcast_to_rule(ctx: LoweringRuleContext, x, shape: Sequence[int]):
  (x_aval,) = ctx.avals_in
  return _bcast_to(_ensure_ir_value(x, x_aval), shape)

