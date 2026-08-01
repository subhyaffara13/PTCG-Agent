
def _mgpu_arrive_op_lowering_rule(
    ctx: LoweringContext, arrive_op: mgpu.ArriveOp
) -> Sequence[ir.Value]:
  barrier = utils.DialectBarrierRef.from_barrier_memref(arrive_op.barrier)
  orders_tc = arrive_op.orders_tensor_core.value
  if orders_tc:
    # Barrier expects a single thread arrival.
    predicate = ctx.single_lane_predicate
    arrival_count = 1
  elif ctx.thread_semantics == utils.ThreadSubset.WARP:
    # In warp-level lowering, we arrive on each CUDA thread in a warp, but the
    # barrier still expects a full 128 arrivals so we arrive 4 times on each
    # CUDA thread instead.
    predicate = None
    arrival_count = 4
  else:
    # Barrier expects each thread arrives once.
    predicate = None
    arrival_count = 1

  barrier.barrier_ref.arrive(
      arrival_count,
      orders_tensor_core=orders_tc,
      predicate=predicate,
      scope=ctx.thread_semantics,
  )
  return []

