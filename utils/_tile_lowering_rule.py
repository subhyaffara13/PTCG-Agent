
def _tile_lowering_rule(ctx: LoweringRuleContext, x, *, reps):
  del ctx  # Unused.
  for axis, repeats in enumerate(reps):
    if repeats > 1:
      x = tpu.concatenate([x] * repeats, dimension=axis)
  return x

