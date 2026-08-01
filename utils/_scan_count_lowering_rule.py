
def _scan_count_lowering_rule(ctx: sc_lowering.LoweringRuleContext, x, mask):
  del ctx  # Unused.
  # Reverse, because the MLIR op returns the mask first.
  return tpu.scan_count(mask, x)[::-1]

