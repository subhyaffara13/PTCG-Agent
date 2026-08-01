
def _wgmma_accumulator_store_warpgroup_lowering(
    ctx: lowering.LoweringRuleContext, acc, val
):
  del ctx, acc
  val = mgpu.dialect.optimization_barrier([val])
  nvvm_dialect.wgmma_fence_aligned()
  return val

