
def _tcgen05_commit_arrive_lowering(
    ctx: lowering.LoweringRuleContext,
    barrier_ref: mgpu.BarrierRef,
    *barrier_transforms_leaves,
    barrier_transforms_tree,
    collective_axis,
):
  barrier_ref_aval = ctx.avals_in[0]
  assert isinstance(barrier_ref_aval, state_types.AbstractRef)
  if barrier_transforms_tree is not None:
    barrier_transforms = barrier_transforms_tree.unflatten(
        barrier_transforms_leaves
    )
    base_index = _get_barrier_base_index(barrier_ref_aval, barrier_transforms)
    if base_index is not None:
      barrier_ref = barrier_ref[base_index]

  predicate = ctx.module_ctx.single_lane_predicate
  if collective_axis is not None:
    assert predicate is not None
    is_leader_block = _collective_mma_predicate(ctx, collective_axis)
    predicate = arith_dialect.andi(predicate, is_leader_block)
    collective = True
  else:
    collective = False

  with mgpu.when(predicate):
    tcgen05.commit_arrive(barrier_ref,
                          collective=collective,
                          ctx=ctx.launch_ctx)
  return []

