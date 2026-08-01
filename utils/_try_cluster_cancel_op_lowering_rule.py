
def _try_cluster_cancel_op_lowering_rule(
    ctx: LoweringContext, op: mgpu.TryClusterCancelOp
) -> Sequence[ir.Value]:
  barrier = utils.DialectBarrierRef.from_barrier_memref(op.barrier)
  predicate = ctx.single_lane_predicate
  if op.predicate is not None:
    predicate = arith.andi(predicate, op.predicate)
  utils.try_cluster_cancel(op.cancellation_result, barrier.barrier_ref, predicate)
  return []

