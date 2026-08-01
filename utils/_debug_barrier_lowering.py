
def _debug_barrier_lowering(ctx: lowering.LoweringRuleContext):
  del ctx  # Unused.
  gpu_dialect.barrier()
  return []

