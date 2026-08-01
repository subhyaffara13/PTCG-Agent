
def _copy_smem_to_gmem_lowering(
    ctx: lowering.LoweringRuleContext,
    src,
    dst,
    *flat_args,
    src_transforms_treedef,
    dst_transforms_treedef,
    has_user_predicate,
    commit_group,
    reduction_op,
):
  if has_user_predicate:
    flat_args, user_predicate = flat_args[:-1], flat_args[-1]
    predicate = lowering._ensure_ir_value(user_predicate, jnp.bool)
  else:
    predicate = None

  flat_src_transforms, flat_dst_transforms = util.split_list(
      flat_args,
      [src_transforms_treedef.num_leaves],
  )
  src_transforms = src_transforms_treedef.unflatten(flat_src_transforms)
  dst_transforms = dst_transforms_treedef.unflatten(flat_dst_transforms)
  handle_transposes = (
      ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Warpgroup
  )
  src_aval = ctx.avals_in[0]
  assert isinstance(src_aval, state_types.AbstractRef)
  src_transform_avals = src_transforms_treedef.unflatten(
      ctx.avals_in[2 : 2 + src_transforms_treedef.num_leaves]
  )
  dst_transform_avals = dst_transforms_treedef.unflatten(
      ctx.avals_in[
          2
          + src_transforms_treedef.num_leaves : 2
          + src_transforms_treedef.num_leaves
          + dst_transforms_treedef.num_leaves
      ]
  )
  src, src_aval, src_transforms = lowering._handle_transforms(
      ctx, src_aval, src, src_transform_avals, src_transforms,
      handle_transposes=handle_transposes
  )
  copy_params = {
      **_extract_gmem_copy_params(ctx, dst_transforms, dst_transform_avals, supports_multicast=True),
      **_extract_smem_copy_params(src_aval, src_transforms),
  }
  is_scatter = False
  if gmem_slice := copy_params.get("gmem_slice", ()):
    first_idx = gmem_slice[0]
    if isinstance(first_idx, mgpu.FragmentedArray) and first_idx.shape:
      is_scatter = True

  if is_scatter:
    if predicate is not None:
      raise NotImplementedError("Gather/scatter TMA does not support predicates yet.")
    if ctx.module_ctx.primitive_semantics == gpu_core.PrimitiveSemantics.Warp:
      raise ValueError("Gather/scatter operations are not supported in a warp context.")

  if ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Lane:
    if not is_scatter:
      lane_pred = ctx.module_ctx.single_lane_predicate
      assert lane_pred is not None  # Satisfy pytype
      if predicate is not None:
        predicate = arith_dialect.andi(predicate, lane_pred)
      else:
        predicate = lane_pred

    ctx.launch_ctx.async_copy(
        src_ref=src,
        dst_ref=dst,
        arrive=commit_group,
        reduction_op=reduction_op,
        oob_mode=OOBFillMode.UNDEFINED,
        **copy_params,
        **(dict(predicate=predicate) if predicate is not None else {}),  # pyrefly: ignore[bad-argument-type]
    )
    return ()

  if gmem_slice := copy_params.get("gmem_slice", ()):
    indices, slice_lengths = _split_gmem_slice(gmem_slice)
  else:
    i32 = ir.IntegerType.get_signless(32)
    slice_lengths = ir.MemRefType(src.type).shape
    indices = [mgpu.utils.c(0, i32)] * len(slice_lengths)

  assert copy_params.get("swizzle") is None
  peer_id = copy_params.get("gmem_peer_id")
  if peer_id is mgpu.GLOBAL_BROADCAST:
    is_global_broadcast = True
    peer_id = None
  else:
    is_global_broadcast = False

  assert not copy_params.get("gmem_transform")
  if reduction_op is not None:
    reduction_op_attr = getattr(mgpu.dialect.TMAReduction, reduction_op.capitalize())
  else:
    reduction_op_attr = None

  mgpu.dialect.async_store(
      src,
      dst,
      indices,
      slice_lengths,
      predicate=predicate,
      commit_group=commit_group,
      reduction_op=reduction_op_attr,
      gmem_peer_id=peer_id,
      is_global_broadcast=is_global_broadcast,
  )
  return ()

