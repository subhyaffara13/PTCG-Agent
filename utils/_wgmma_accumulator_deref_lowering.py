
def _wgmma_accumulator_deref_lowering(
    ctx: lowering.LoweringRuleContext, acc, *, wait_n: int | None
):
  if wait_n is not None:
    nvvm_dialect.wgmma_wait_group_sync_aligned(wait_n)
  return (
      acc.value
      if ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Lane
      else acc
  )

