
def _store_lowering_rule(
    ctx: LoweringRuleContext, ref, val, mask, *flat_transforms, tree, add
):
  ref_aval, _, *_flat_index_avals = ctx.avals_in
  assert isinstance(ref_aval, state.AbstractRef)
  [out_aval] = ctx.avals_out
  assert isinstance(out_aval, jax_core.ShapedArray)

  ref_memory_space = tpu_core.memory_space_to_tpu_memory_space(
      ref_aval.memory_space, ctx.lowering_context.kernel_type
  )
  if (
      ref_memory_space is MemorySpace.HBM
      or ref_memory_space is MemorySpace.VMEM_SHARED
  ):
    raise NotImplementedError(
        f"Swap does not support storing to {ref_memory_space!r}."
        " Copy the data to a core-local memory space, e.g. VMEM,"
        " via `pltpu.async_copy`."
    )

  transforms = list(tree_util.tree_unflatten(tree, flat_transforms))
  if not transforms or not isinstance(transforms[-1], indexing.NDIndexer):
    tref_aval = state.transform_type(transforms, ref_aval)
    assert isinstance(tref_aval, state.AbstractRef)
    transforms.append(indexing.NDIndexer.make_trivial_indexer(tref_aval.shape))
  *prev_transforms, indexer = transforms
  ref_block_shape, *_ = ctx.block_shapes
  ref, ref_block_shape = _transform_ref(
      ref, ref_aval, ref_block_shape, prev_transforms
  )
  starts, sizes, strides, squeeze_dims, _ = tc_lowering._indexer_to_start_size_stride(
      indexer, ref_block_shape, cast_to_index=True
  )
  for first_nontrivial_dim, s in enumerate(sizes):
    if s != 1:
      break
  else:
    first_nontrivial_dim = len(sizes)
  if any(squeeze_dims[first_nontrivial_dim:]):
    raise NotImplementedError(
        "Integer indexing of refs that follows a non-trivial slice is not"
        " supported on SC"
    )
  if not all(s == 1 for s in strides):
    raise NotImplementedError(
        "Swap only supports slices with stride 1, got {strides}"
    )

  if (out_aval.ndim == 0) != (ref_memory_space is MemorySpace.SMEM):
    message = "Swap only supports scalars in SMEM."
    if ref_memory_space is MemorySpace.SMEM:
      message += " Trying to swap an array of shape {out_aval.shape}."
    else:
      message += f" Trying to swap a scalar in {ref_memory_space!r}."
    raise NotImplementedError(message)

  if out_aval.ndim == 0:
    if mask is not None:
      raise NotImplementedError("Swap does not support masked scalar stores")
    if add:
      # TODO(slebedev): We can use memref.atomic_rmw here, but the SC compiler
      # doesn't support it yet.
      raise NotImplementedError("Swap does not support atomic scalar adds")
    old_val = memref.load(ref, starts)
    memref.store(val, ref, starts)
    return old_val

  if not ctx.lowering_context.needs_layout_passes:
    _check_aval_is_supported("Swap", out_aval)
  out_vec_type = ir.VectorType.get(
      out_aval.shape, _dtype_to_ir_type(out_aval.dtype)
  )
  if not ctx.lowering_context.needs_layout_passes:
    old_val = tpu.vector_load(out_vec_type, ref, starts, strides=[], mask=mask)
    _ = tpu.vector_store(
        val, ref, indices=starts, strides=[], mask=mask, add=add
    )
    return old_val
  # Load and store at the full memref rank, keeping integer-indexed dims as
  # size 1, because apply-vector-layout requires the vector rank to match
  # the memref.
  memref_vec_shape = cast(
      Sequence[int],
      [1 if squeeze else s for s, squeeze in zip(sizes, squeeze_dims)],
  )
  memref_vec_type = ir.VectorType.get(
      memref_vec_shape, _dtype_to_ir_type(out_aval.dtype)
  )
  old_val = tpu.vector_load(memref_vec_type, ref, starts, strides=[], mask=mask)
  old_val = vector.shape_cast(out_vec_type, old_val)
  val_memref_rank = vector.shape_cast(memref_vec_type, val)
  tpu.vector_store(val_memref_rank, ref, starts, strides=[], mask=mask, add=add)
  return old_val

