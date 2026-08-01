
def _tcgen05_commit_arrive_lowering_wg(
    ctx: lowering.LoweringRuleContext,
    barrier_ref: mgpu.DialectBarrierRef,
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

  predicate_ctx: contextlib.AbstractContextManager[None]
  if collective_axis is not None:
    predicate_ctx = mgpu.when(_collective_mma_predicate(ctx, collective_axis))
    collective = True
  else:
    predicate_ctx = contextlib.nullcontext()
    collective = False

  with predicate_ctx:
    mgpu.dialect.tcgen05_commit_arrive(
        barrier_ref.as_barrier_memref(), collective=collective
    )
  return []

