
def _async_copy_to_tmem_lowering_rule(
    impl, ctx: lowering.LoweringRuleContext, smem_ref, tmem_ref, *leaves, smem_tree, tmem_tree, collective_axis
):
  if ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Lane:
    assert isinstance(tmem_ref, tcgen05.TMEMRef)
  smem_leaves, tmem_leaves = util.split_list(leaves, [smem_tree.num_leaves])
  smem_transforms = jax.tree.unflatten(smem_tree, smem_leaves)
  tmem_transforms = jax.tree.unflatten(tmem_tree, tmem_leaves)
  smem_aval = ctx.avals_in[0]
  assert isinstance(smem_aval, state_types.AbstractRef)
  tmem_aval = ctx.avals_in[1]
  assert isinstance(tmem_aval, state_types.AbstractRef)
  transform_avals = util.split_list(
      ctx.avals_in[2:], [smem_tree.num_leaves]
  )
  smem_transform_avals = smem_tree.unflatten(transform_avals[0])
  tmem_transform_avals = tmem_tree.unflatten(transform_avals[1])
  smem_ref, _, smem_transforms = lowering._handle_transforms(
      ctx, smem_aval, smem_ref, smem_transform_avals, smem_transforms
  )
  tmem_ref, _, tmem_transforms = lowering._handle_transforms(
      ctx, tmem_aval, tmem_ref, tmem_transform_avals, tmem_transforms
  )
  if smem_transforms:
    raise NotImplementedError(f"Unimplemented transforms for SMEM refs: {smem_transforms}")
  if tmem_transforms:
    raise NotImplementedError(f"Unimplemented transforms for TMEM refs: {tmem_transforms}")

  if ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Warpgroup:
    predicate_ctx: contextlib.AbstractContextManager[None]
    if collective_axis is not None:
      predicate_ctx = mgpu.when(_collective_mma_predicate(ctx, collective_axis))
      collective = True
    else:
      predicate_ctx = contextlib.nullcontext()
      collective = False
    with predicate_ctx:
      impl(smem_ref, tmem_ref, collective=collective)
    return ()

  predicate = ctx.module_ctx.single_lane_predicate
  if collective_axis is not None:
    assert predicate is not None
    is_leader_block = _collective_mma_predicate(ctx, collective_axis)
    predicate = arith_dialect.andi(predicate, is_leader_block)
    collective = True
  else:
    collective = False

  with mgpu.when(predicate):
    impl(smem_ref, tmem_ref, collective=collective)
  return ()

