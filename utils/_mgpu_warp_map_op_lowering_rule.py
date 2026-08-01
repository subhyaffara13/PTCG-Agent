
def _mgpu_warp_map_op_lowering_rule(
    ctx: LoweringContext, op: mgpu.WarpMapOp
) -> Sequence[ir.Value]:
  """Lowering rule for mgpu.WarpMapOp."""
  for a, o in zip(op.body.arguments, op.operands, strict=True):
    a.replace_all_uses_with(o)
  warp_ctx = dataclasses.replace(ctx, thread_semantics=utils.ThreadSubset.WARP)
  # We allow the warps to schedule async copies without synchronizing with
  # other warps, so we need to add a barrier here to make sure all reads and
  # writes have completed.
  if ctx.auto_barriers:
    utils.warpgroup_barrier()
  ip = ir.InsertionPoint.current
  for op in op.body.operations:
    op.detach_from_parent()
    ip.insert(op)
    warp_ctx.lower_op(op)
  # We need to ensure that any effects produced by one warp (e.g. async copies)
  # are observable by all other warps.
  if ctx.auto_barriers:
    utils.warpgroup_barrier()
  return []

