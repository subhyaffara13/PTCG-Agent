
def _commit_smem_lowering(ctx: lowering.LoweringRuleContext):
  # TODO(bchetioui): add primitive for commit smem to mosaic_gpu dialect.
  mgpu.commit_shared()
  return ()

