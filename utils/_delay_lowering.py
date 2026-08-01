
def _delay_lowering(ctx: LoweringRuleContext, nanos):
  del ctx  # Unused.
  if not isinstance(nanos, ir.Value):
    nanos = _i32_constant(nanos)
  mgpu.nanosleep(nanos)
  return []

