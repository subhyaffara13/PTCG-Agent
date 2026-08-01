
def _tcgen05_commit_arrive_op_lowering_rule(
    ctx: LoweringContext, op: mgpu.TcGen05CommitArriveOp
) -> Sequence[ir.Value]:
  """Lowering rule for mgpu.TcGen05CommitArriveOp."""
  ctx.check_collective(op)
  barrier = utils.DialectBarrierRef.from_barrier_memref(op.barrier)
  with utils.when(ctx.single_lane_predicate):
    tcgen05.commit_arrive(
        barrier.barrier_ref, op.collective.value, ctx.launch_context
    )
  return []

