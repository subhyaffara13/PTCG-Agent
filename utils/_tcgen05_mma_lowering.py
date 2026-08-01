
def _tcgen05_mma_lowering(
    ctx: lowering.LoweringRuleContext,
    acc: tcgen05.TMEMRef,
    a_ref,
    b_ref,
    accumulate: bool | ir.Value,
    *barrier_scales_and_transforms_leaves,
    acc_transforms_tree,
    a_transforms_tree,
    b_transforms_tree,
    barrier_transforms_tree,
    a_scale_transforms_tree,
    b_scale_transforms_tree,
    a_sparse_metadata_transforms_tree,
    collective_axis,
    arrive,
    scaled: bool,
    sparse: bool,
):
  (
      acc_aval,
      a_aval,
      b_aval,
      accumulate_aval,
      *_,
  ) = ctx.avals_in
  assert isinstance(acc_aval, state_types.AbstractRef)
  assert isinstance(a_aval, state_types.AbstractRef)
  assert isinstance(b_aval, state_types.AbstractRef)
  del accumulate_aval
  lhs_swizzle: int | None = None
  lhs_transpose: bool = False
  leaves = list(barrier_scales_and_transforms_leaves)
  avals = list(ctx.avals_in[4:])
  if arrive:
    barrier_ref, leaves = leaves[0], leaves[1:]
    barrier_ref_aval, avals = avals[0], avals[1:]
  else:
    barrier_ref = None
    barrier_ref_aval = None
  if scaled:
    a_scale_ref, b_scale_ref, leaves = leaves[0], leaves[1], leaves[2:]
    a_scale_ref_aval, b_scale_ref_aval, avals = avals[0], avals[1], avals[2:]
  else:
    a_scale_ref = b_scale_ref = a_scale_ref_aval = b_scale_ref_aval = None
  if sparse:
    a_sparse_metadata_ref, leaves = leaves[0], leaves[1:]
    a_sparse_metadata_ref_aval, avals = avals[0], avals[1:]
  else:
    a_sparse_metadata_ref = a_sparse_metadata_ref_aval = None

  transforms_trees = (
      acc_transforms_tree,
      a_transforms_tree,
      b_transforms_tree,
      barrier_transforms_tree,
      a_scale_transforms_tree,
      b_scale_transforms_tree,
      a_sparse_metadata_transforms_tree,
  )
  ns = [getattr(tree, "num_leaves", 0) for tree in transforms_trees]
  transforms_leaves_lists = util.split_list_checked(leaves, ns)
  transforms_avals_lists = util.split_list_checked(avals, ns)

  (
      acc_transforms_leaves,
      a_transforms_leaves,
      b_transforms_leaves,
      barrier_transforms_leaves,
      a_scale_transforms_leaves,
      b_scale_transforms_leaves,
      a_sparse_metadata_transforms_leaves,
  ) = transforms_leaves_lists

  (
      acc_transforms_leaves_avals,
      a_transforms_leaves_avals,
      b_transforms_leaves_avals,
      barrier_transforms_leaves_avals,
      a_scale_transforms_leaves_avals,
      b_scale_transforms_leaves_avals,
      a_sparse_metadata_transforms_leaves_avals,
  ) = transforms_avals_lists

  if acc_transforms_tree is not None:
    acc_transforms = acc_transforms_tree.unflatten(acc_transforms_leaves)
    acc_transform_avals = acc_transforms_tree.unflatten(acc_transforms_leaves_avals)
    acc, _, acc_transforms = lowering._handle_transforms(
        ctx, acc_aval, acc, acc_transform_avals, acc_transforms,
        handle_transposes=False
    )
    if acc_transforms:
      raise NotImplementedError(
          f"Unsupported transforms for ACC: {acc_transforms}."
      )

  if a_transforms_tree is not None:
    a_transforms = a_transforms_tree.unflatten(a_transforms_leaves)
    a_out_ty = state_types.transform_type(a_transforms, a_aval)
    assert isinstance(a_out_ty, state_types.AbstractRef)
    a_dtype = a_out_ty.dtype
    a_transform_avals = a_transforms_tree.unflatten(a_transforms_leaves_avals)
    a_ref, _, a_transforms = lowering._handle_transforms(
        ctx, a_aval, a_ref, a_transform_avals, a_transforms,
        handle_transposes=False, handle_reshapes=True)
    match a_transforms:
      case (
          gpu_core.UnswizzleRef(lhs_swizzle),
          gpu_core.UntilingTransform(lhs_tiling),
      ):
        lhs_transpose = False
      case (
          gpu_core.UnswizzleRef(lhs_swizzle),
          gpu_core.UntilingTransform(lhs_tiling),
          state_types.TransposeTransform((1, 0)),
      ):
        lhs_transpose = True
      case () if isinstance(a_ref, tcgen05.TMEMRef):
        lhs_tiling = None
      case _:
        raise NotImplementedError(
            f"Unsupported transforms for LHS: {a_transforms}."
        )
    if not isinstance(a_ref, tcgen05.TMEMRef):
      assert lhs_swizzle is not None
      swizzle_elems = 8 * lhs_swizzle // dtypes.itemsize_bits(a_dtype)
      if lhs_tiling != (8, swizzle_elems):
        raise ValueError("MMA lhs tiling does not fit swizzle. "
                        f"{lhs_tiling=} expected={(8, swizzle_elems)}")

  assert b_transforms_tree is not None
  b_transforms = b_transforms_tree.unflatten(b_transforms_leaves)
  b_out_ty = state_types.transform_type(b_transforms, b_aval)
  assert isinstance(b_out_ty, state_types.AbstractRef)
  b_dtype = b_out_ty.dtype
  b_transform_avals = b_transforms_tree.unflatten(b_transforms_leaves_avals)
  b_ref, _, b_transforms = lowering._handle_transforms(
      ctx, b_aval, b_ref, b_transform_avals, b_transforms, handle_transposes=False,
      handle_reshapes=True)
  match b_transforms:
    case (
        gpu_core.UnswizzleRef(rhs_swizzle),
        gpu_core.UntilingTransform(rhs_tiling),
    ):
      rhs_transpose = False
    case (
        gpu_core.UnswizzleRef(rhs_swizzle),
        gpu_core.UntilingTransform(rhs_tiling),
        state_types.TransposeTransform((1, 0)),
    ):
      rhs_transpose = True
    case _:
      raise NotImplementedError(
          f"Unsupported transforms for RHS: {b_transforms}."
      )
  swizzle_elems = 8 * rhs_swizzle // dtypes.itemsize_bits(b_dtype)
  if rhs_tiling != (8, swizzle_elems):
    raise ValueError(
        "MMA rhs tiling does not fit swizzle"
        f" {rhs_tiling=} expected={(8, swizzle_elems)}"
    )

  if barrier_transforms_tree is not None and barrier_ref is not None:
    barrier_transforms = barrier_transforms_tree.unflatten(
        barrier_transforms_leaves
    )
    base_index = _get_barrier_base_index(barrier_ref_aval, barrier_transforms)
    if base_index is not None:
      barrier_ref = barrier_ref[base_index]

  if lhs_swizzle is None:
    lhs_swizzle = rhs_swizzle
  elif rhs_swizzle != lhs_swizzle:
    raise ValueError("MMA rhs swizzle must match lhs swizzle."
                      f" {lhs_swizzle=} {rhs_swizzle=}")
  if lhs_transpose:
    if isinstance(a_ref, tcgen05.TMEMRef):
      raise ValueError("TMEM transpose not allowed.")
    a_ref = mgpu.memref_transpose(a_ref, (1, 0, 3, 2))
  if rhs_transpose:
    b_ref = mgpu.memref_transpose(b_ref, (1, 0, 3, 2))
  if isinstance(accumulate, bool):
    accumulate = mgpu.c(accumulate, ir.IntegerType.get_signless(1))
  elif isinstance(accumulate, mgpu.FragmentedArray):
    accumulate = accumulate.registers.item()
    assert isinstance(accumulate, ir.Value)

  if a_scale_ref is not None and a_scale_transforms_tree is not None:
    assert isinstance(a_scale_ref_aval, state.AbstractRef)
    a_scale_transforms = a_scale_transforms_tree.unflatten(
        a_scale_transforms_leaves
    )
    a_scale_transform_avals = a_scale_transforms_tree.unflatten(
        a_scale_transforms_leaves_avals
    )
    a_scale_ref, _, a_scale_transforms = lowering._handle_transforms(
        ctx, a_scale_ref_aval, a_scale_ref, a_scale_transform_avals,
        a_scale_transforms
    )
    if a_scale_transforms:
      raise NotImplementedError(
          f"Unsupported transforms: {a_scale_transforms}"
      )
  if b_scale_ref is not None and b_scale_transforms_tree is not None:
    assert isinstance(b_scale_ref_aval, state.AbstractRef)
    b_scale_transforms = b_scale_transforms_tree.unflatten(
        b_scale_transforms_leaves
    )
    b_scale_transform_avals = b_scale_transforms_tree.unflatten(
        b_scale_transforms_leaves_avals
    )
    b_scale_ref, _, b_scale_transforms = lowering._handle_transforms(
        ctx, b_scale_ref_aval, b_scale_ref, b_scale_transform_avals,
        b_scale_transforms
    )
    if b_scale_transforms:
      raise NotImplementedError(f"Unsupported transforms: {b_scale_transforms}")
  if a_sparse_metadata_transforms_tree is not None:
    a_sparse_metadata_transforms = a_sparse_metadata_transforms_tree.unflatten(
        a_sparse_metadata_transforms_leaves
    )
    a_sparse_metadata_transform_avals = (
        a_sparse_metadata_transforms_tree.unflatten(
            a_sparse_metadata_transforms_leaves_avals
        )
    )
    assert isinstance(a_sparse_metadata_ref_aval, state_types.AbstractRef)
    a_sparse_metadata_ref, _, a_sparse_metadata_transforms = (
        lowering._handle_transforms(  # pyrefly: ignore[bad-specialization]
            ctx, a_sparse_metadata_ref_aval, a_sparse_metadata_ref,
            a_sparse_metadata_transform_avals, a_sparse_metadata_transforms)
    )
    if a_sparse_metadata_transforms:
      raise NotImplementedError(
          f"Unsupported transforms: {a_sparse_metadata_transforms}"
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
    tcgen05.mma(
        acc,
        a_ref,
        b_ref,
        a_swizzle=int(lhs_swizzle),
        b_swizzle=int(rhs_swizzle),
        a_scale=a_scale_ref,
        b_scale=b_scale_ref,
        a_sparse_metadata=a_sparse_metadata_ref,
        accumulate=accumulate,
        collective=collective,
    )
    if arrive:
      assert barrier_ref is not None
      tcgen05.commit_arrive(barrier_ref,
                            collective=collective,
                            ctx=ctx.launch_ctx)
  return []

