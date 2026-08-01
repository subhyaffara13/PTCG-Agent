
def _tmem_relinquish_alloc_permit_op_lowering_rule(
    ctx: LoweringContext, op: mgpu.TmemRelinquishAllocPermitOp
) -> Sequence[ir.Value]:
  """Lowering rule for mgpu.TmemRelinquishAllocPermitOp."""
  ctx.check_collective(op)
  with utils.when(ctx.single_warp_per_block_predicate):
    tcgen05.tmem_relinquish_alloc_permit(bool(op.collective))
  return []

