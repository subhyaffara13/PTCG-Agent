
def _wgmma_lowering(
    ctx: lowering.LoweringRuleContext,
    acc,
    a,
    b,
    *transforms_leaves,
    acc_transforms_tree,
    a_transforms_tree,
    b_transforms_tree,
):
  lhs_swizzle: int | None = None
  transform_treedefs = [
      acc_transforms_tree, a_transforms_tree, b_transforms_tree
  ]
  transform_leaves = util.split_list(
      transforms_leaves, [getattr(tree, "num_leaves", 0) for tree in transform_treedefs]
  )
  acc_transforms, a_transforms, b_transforms = (
      None if treedef is None else treedef.unflatten(leaves)
      for treedef, leaves in zip(transform_treedefs, transform_leaves)
  )

  acc_indices = None
  if acc_transforms is not None:
    if not all(isinstance(t, indexing.NDIndexer) for t in acc_transforms):
      raise ValueError("WGMMA accumulator only supports indexing transforms")
    acc_indexer = lowering.merge_indexers(acc_transforms)
    if acc_indexer.int_indexer_shape:
      raise NotImplementedError("int_indexer_shape non-empty")
    acc_indices = lowering._ndindexer_indices(acc_indexer)

  transform_avals_list = util.split_list(
      ctx.avals_in[3:], [getattr(tree, "num_leaves", 0) for tree in transform_treedefs]
  )
  if a_transforms is not None:
    a_aval = ctx.avals_in[1]
    if not isinstance(a_aval, state_types.AbstractRef):
      assert isinstance(a_aval, jax_core.ShapedArray), (type(a_aval),)
      a_ref_aval = state.AbstractRef(a_aval)
    else:
      a_ref_aval = a_aval
    assert transform_treedefs[1] is not None
    a_transform_avals = transform_treedefs[1].unflatten(transform_avals_list[1])
    a, _, a_transforms = lowering._handle_transforms(
        ctx, a_ref_aval, a, a_transform_avals, a_transforms,
        handle_transposes=False, handle_reshapes=False)
    match a_transforms:
      case (gpu_core.UnswizzleRef(lhs_swizzle), gpu_core.UntilingTransform(tiling)):
        lhs_transpose = False
      case (
          gpu_core.UnswizzleRef(lhs_swizzle),
          gpu_core.UntilingTransform(tiling),
          state_types.TransposeTransform((1, 0)),
      ):
        lhs_transpose = True
      case _:
        raise ValueError(f"WGMMA lhs has unsupported transforms: {a_transforms}.")
    a_mlir_dtype = ir.MemRefType(a.type).element_type
    swizzle_elems = lhs_swizzle // mgpu_utils.bytewidth(a_mlir_dtype)
    if tiling != (8, swizzle_elems):
      raise NotImplementedError(
          f"WGMMA lhs tiling does not fit swizzle. Got {tiling=}, expected (8, {swizzle_elems})"
      )
  else:
    lhs_transpose = False
    if not isinstance(a, mgpu.FragmentedArray):
      raise ValueError(
          "When WGMMA lhs is passed in as a ref, it must be transformed by"
          " swizzling and tiling appropriately."
      )

  assert b_transforms is not None
  b_aval = ctx.avals_in[2]
  if not isinstance(b_aval, state_types.AbstractRef):
    assert isinstance(b_aval, jax_core.ShapedArray)
    b_ref_aval = state_types.AbstractRef(b_aval)
  else:
    b_ref_aval = b_aval
  assert transform_treedefs[2] is not None
  b_transform_avals = transform_treedefs[2].unflatten(transform_avals_list[2])
  b, _, b_transforms = lowering._handle_transforms(
      ctx, b_ref_aval, b, b_transform_avals, b_transforms,
      handle_transposes=False)

  match b_transforms:
    case (gpu_core.UnswizzleRef(rhs_swizzle), gpu_core.UntilingTransform(rhs_tiling)):
      rhs_transpose = False
    case (
        gpu_core.UnswizzleRef(rhs_swizzle),
        gpu_core.UntilingTransform(rhs_tiling),
        state_types.TransposeTransform((1, 0)),
    ):
      rhs_transpose = True
    case _:
      raise ValueError(f"WGMMA rhs has unsupported transforms: {b_transforms}.")

  if lhs_swizzle is not None:
    b_mlir_dtype = ir.MemRefType(b.type).element_type
    swizzle_elems = rhs_swizzle // mgpu_utils.bytewidth(b_mlir_dtype)
    if rhs_swizzle != lhs_swizzle:
      raise NotImplementedError("WGMMA rhs swizzle must match lhs swizzle")
    if rhs_tiling != (8, swizzle_elems):
      raise NotImplementedError("WGMMA rhs tiling does not fit swizzle")

  if lhs_transpose:
    assert isinstance(a, ir.Value)
    a = mgpu.memref_transpose(a, (1, 0, 3, 2))
  if rhs_transpose:
    b = mgpu.memref_transpose(b, (1, 0, 3, 2))
  acc_in = acc
  if acc_indices is not None:
    acc_in = mgpu.WGMMAAccumulator(
        _value=acc._value[acc_indices],
        _original_layout=acc._original_layout,
        _sync=False,
    )
  acc_out = mgpu.wgmma(acc_in, a, b, swizzle=rhs_swizzle)
  if acc_indices is not None:
    acc_value = acc._value.copy()
    acc_value[acc_indices] = acc_out._value
    acc_out = mgpu.WGMMAAccumulator(
        _value=acc_value, _original_layout=acc._original_layout, _sync=False
    )
  nvvm_dialect.wgmma_commit_group_sync_aligned()
  return acc_out

