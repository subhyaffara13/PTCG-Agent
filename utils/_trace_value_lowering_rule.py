
def _trace_value_lowering_rule(ctx: LoweringRuleContext, value, *, label: str):
  """Lower trace_value to tpu.trace_value."""
  del ctx
  tpu.trace_value(value, label)
  return []

