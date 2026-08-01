
def _initialize_barrier_op_lowering_rule(
    ctx: LoweringContext,
    op: mgpu.InitializeBarrierOp,
) -> Sequence[ir.Value]:
  i32 = ir.IntegerType.get_signless(32)
  arrival_count = op.arrival_count.value * (
      utils.WARPGROUP_SIZE if not op.orders_tensor_core.value else 1
  )
  for i in range(op.num_barriers.value):
    nvvm.mbarrier_init(
        utils.getelementptr(op.base_pointer, [i], _lowered_barrier_type()),
        utils.c(arrival_count, i32),
        predicate=ctx.single_thread_per_block_predicate,
    )
  return []

