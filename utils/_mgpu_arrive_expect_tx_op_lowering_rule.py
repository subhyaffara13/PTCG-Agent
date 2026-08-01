
def _mgpu_arrive_expect_tx_op_lowering_rule(
    ctx: LoweringContext, arrive_expect_tx_op: mgpu.ArriveExpectTxOp
) -> Sequence[ir.Value]:
  num_bytes: int = arrive_expect_tx_op.expect_tx.value
  i32 = ir.IntegerType.get_signless(32)
  num_lanes = (
      utils.WARPGROUP_SIZE
      if ctx.thread_semantics == utils.ThreadSubset.WARPGROUP
      else utils.WARP_SIZE
  )
  if num_bytes % num_lanes == 0:
    # Prefer uniform arrival whenever possible because it's more efficient.
    # We arrive uniformly from each lane in the WG/Warp, so we need to divide
    # the number of bytes by the number of lanes in the WG/Warp.
    tx_bytes = utils.c(num_bytes // num_lanes, i32)
  else:
    tx_bytes = arith.select(
        ctx.single_lane_predicate,
        utils.c(num_bytes, i32),
        utils.c(0, i32),
    )

  barrier = utils.DialectBarrierRef.from_barrier_memref(
      arrive_expect_tx_op.barrier
  )
  # In Warp-level lowering, we arrive on each CUDA thread in a warp, but the
  # barrier still expects a full 128 arrivals so we arrive 4 times on each CUDA
  # thread instead.
  if ctx.thread_semantics == utils.ThreadSubset.WARP:
    barrier.barrier_ref.arrive(arrival_count=3, can_complete=False)
  barrier.barrier_ref.arrive_expect_tx(tx_bytes)

  return []

