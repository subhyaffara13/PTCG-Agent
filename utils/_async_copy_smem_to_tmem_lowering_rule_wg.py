
def _async_copy_smem_to_tmem_lowering_rule_wg(
    ctx: lowering.LoweringRuleContext, smem_ref, tmem_ref, *leaves,
    smem_tree, tmem_tree, collective_axis,
):
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
      ctx, smem_aval, smem_ref, smem_transform_avals, smem_transforms,
      handle_transposes=False
  )
  if smem_transforms:
    raise NotImplementedError(
        f"Unimplemented transforms for SMEM ref: {smem_transforms}"
    )
  tmem_ref, _, tmem_transforms = lowering._handle_transforms(
      ctx, tmem_aval, tmem_ref, tmem_transform_avals, tmem_transforms
  )
  if tmem_transforms:
    raise NotImplementedError(
        f"Unimplemented transforms for TMEM refs: {tmem_transforms}"
    )

  predicate_ctx: contextlib.AbstractContextManager[None]
  if collective_axis is not None:
    predicate_ctx = mgpu.when(_collective_mma_predicate(ctx, collective_axis))
    collective = True
  else:
    predicate_ctx = contextlib.nullcontext()
    collective = False

  with predicate_ctx:
    mgpu.dialect.async_store_smem_to_tmem(
        smem_ref, tmem_ref, collective=collective
    )

  return []

