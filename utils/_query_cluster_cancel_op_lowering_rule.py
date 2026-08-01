
def _query_cluster_cancel_op_lowering_rule(
    ctx: LoweringContext, op: mgpu.QueryClusterCancelOp
) -> Sequence[ir.Value]:
  del ctx
  return utils.query_cluster_cancel(op.cancellation_result)

