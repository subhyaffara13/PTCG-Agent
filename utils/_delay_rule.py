
def _delay_rule(ctx: LoweringRuleContext, nanos: ir.Value):
  tpu.delay(nanos)
  return []

