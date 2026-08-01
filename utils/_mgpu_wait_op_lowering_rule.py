
def _mgpu_wait_op_lowering_rule(
    _: LoweringContext, wait_op: mgpu.WaitOp
) -> Sequence[ir.Value]:

  barrier = utils.DialectBarrierRef.from_barrier_memref(wait_op.barrier)
  barrier.wait_parity(wait_op.parity)

  return []

