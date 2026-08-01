
def _commit_group_lowering(ctx: lowering.LoweringRuleContext):
  del ctx  # Unused.
  nvvm_dialect.cp_async_bulk_commit_group()
  return ()

