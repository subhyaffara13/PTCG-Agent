
def _wgmma_accumulator_store_lowering(
    ctx: lowering.LoweringRuleContext, acc, val
):
  del ctx, acc
  return mgpu.WGMMAAccumulator.from_registers(val)

