
def _layout_cast_lowering(ctx: LoweringRuleContext, x, *, new_layout):
  del ctx  # Unused.
  return x.to_layout(new_layout.to_mgpu())

