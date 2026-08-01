
def _async_copy_smem_to_tmem_lowering_rule(
    ctx: lowering.LoweringRuleContext, smem_ref, tmem_ref, *leaves,
    smem_tree, tmem_tree, collective_axis,
):
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
  smem_ref, transformed_smem_aval, smem_transforms = lowering._handle_transforms(
      ctx, smem_aval, smem_ref, smem_transform_avals, smem_transforms,
      handle_transposes=False
  )
  tmem_ref, _, tmem_transforms = lowering._handle_transforms(
      ctx, tmem_aval, tmem_ref, tmem_transform_avals, tmem_transforms
  )
  match smem_transforms:
    case (
        gpu_core.UnswizzleRef(swizzle),
        gpu_core.UntilingTransform(tiling),
    ):
      pass
    case (gpu_core.UntilingTransform(tiling),):
      swizzle = 16  # swizzle=16 is equivalent to no swizzle.
    case _:
      raise NotImplementedError(
          f"Unsupported transforms for SMEM ref: {smem_transforms}"
      )
  swizzle_elems = 8 * swizzle // dtypes.itemsize_bits(transformed_smem_aval.dtype)
  if tiling != (8, swizzle_elems):
    raise ValueError(
        f"Tiling does not fit swizzle: expected (8, {swizzle_elems}), but got"
        f" {tiling}"
    )
  if tmem_transforms:
    raise NotImplementedError(
        f"Unimplemented transforms for TMEM refs: {tmem_transforms}"
    )

  predicate = ctx.module_ctx.single_lane_predicate
  if collective_axis is not None:
    assert predicate is not None
    is_leader_block = _collective_mma_predicate(ctx, collective_axis)
    predicate = arith_dialect.andi(predicate, is_leader_block)
    collective = True
  else:
    collective = False

  with mgpu.when(predicate):
    tcgen05.async_copy_smem_to_tmem(
        smem_ref, tmem_ref, swizzle, collective=collective
    )
  return ()

