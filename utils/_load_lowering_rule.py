
def _load_lowering_rule(ctx: LoweringRuleContext, *args_flat, args_tree, **_):
  ref, transforms, mask, _ = args_tree.unflatten(args_flat)
  ref_aval, transforms_avals, _, _ = args_tree.unflatten(ctx.avals_in)
  prev_transforms, idx = _canonicalize_transforms_to_indexer(
      ref_aval, transforms, transforms_avals
  )
  if mask is not None:
    raise NotImplementedError

  ref_block_shape, *_ = ctx.block_shapes
  ref, ref_block_shape = _transform_ref(
      ref, ref_aval, ref_block_shape, prev_transforms
  )
  ref_type = ir.MemRefType(ref.type)
  is_smem_load = str(ref_type.memory_space) == "#tpu.memory_space<smem>"
  (aval_out,) = ctx.avals_out
  if isinstance(aval_out.dtype, prng.KeyTy) and pl_random.is_pallas_impl(
      aval_out.dtype._impl
  ):
    # TODO(justinfu): Merge this with standard extended dtype handling.
    if not is_smem_load:
      raise ValueError("PRNG keys must be loaded from SMEM. Did you set "
                       "the memory space to MemorySpace.SMEM in the "
                       "BlockSpec for the PRNG key input?")
    return _prng_key_load_lowering_rule(ctx, *args_flat, args_tree=args_tree)
  if should_physicalize_dtype(aval_out.dtype):
    # pyrefly: ignore[bad-argument-type]
    physical_element_aval = jax_core.physical_element_aval(aval_out.dtype)
    idx = cast(NDIndexer, idx)
    if idx.int_indexer_shape:
      raise NotImplementedError()
    elt_slices = [
        indexing.Slice(0, size) for size in physical_element_aval.shape]
    idx = NDIndexer(
        indices=idx.indices + tuple(elt_slices),
        shape=idx.shape + physical_element_aval.shape,
        int_indexer_shape=(),
    )
    physical_out_dtype = physical_element_aval.dtype
    physical_out_shape = jax_core.physical_shape(
        aval_out.shape, aval_out.dtype
    )
  else:
    physical_out_dtype = aval_out.dtype
    physical_out_shape = aval_out.shape
  if not is_smem_load and not ref_block_shape:
    raise NotImplementedError(
        "Indexing into a ()-shaped Ref not yet supported on TPU.")
  starts, sizes, strides, _, _ = _indexer_to_start_size_stride(
      idx,
      ref_block_shape,
      cast_to_index=True,
  )
  need_stride = not all((s is None or s == 1) for s in strides)
  if is_smem_load:
    if ctx.avals_out[0].shape:
      raise ValueError("Can only load scalars from SMEM")
    return _maybe_cast_load_to_bool(ctx, aval_out, memref.load(ref, starts))
  elif str(ref_type.memory_space) != "#tpu.memory_space<vmem>":
    extra = ""
    if str(ref_type.memory_space) == "#tpu.memory_space<any>":
      extra = " ANY memory space can only be accessed using async_copy."
    raise ValueError(
        "Loads are only allowed on VMEM and SMEM references." + extra
    )
  load_aval = jax_core.ShapedArray(sizes, dtype=physical_out_dtype)
  if need_stride:
    load_val = tpu.strided_load(
        ctx.aval_to_ir_type(load_aval, is_kernel_boundary=True),
        ref,
        starts,
        strides,
    )
  else:
    load_val = vector.load(
        ctx.aval_to_ir_type(load_aval, is_kernel_boundary=True),
        ref,
        starts,
    )
  if load_aval != aval_out:
    if physical_out_shape:
      vec_type = ir.VectorType.get(
          ctx.lowering_context.dynamic_shape_replacement_fn(
              physical_out_shape
          ),
          _dtype_to_ir_type(physical_out_dtype,
                            is_kernel_boundary=True))
      load_val = vector.shape_cast(vec_type, load_val)
    else:
      load_val = vector.extract(load_val, [], [0] * len(load_aval.shape))
  return _maybe_cast_load_to_bool(ctx, aval_out, load_val)


def _load_lowering_rule(
    ctx: LoweringRuleContext, ref, mask, *flat_transforms, tree
):
  ref_aval, *_flat_index_avals = ctx.avals_in
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
        f"Get does not support loading from {ref_memory_space!r}."
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
        "Get only supports slices with stride 1, got {strides}"
    )

  if (out_aval.ndim == 0) != (ref_memory_space is MemorySpace.SMEM):
    message = "Get only supports loading scalars from SMEM."
    if ref_memory_space is MemorySpace.SMEM:
      message += " Trying to load an array of shape {out_aval.shape}."
    elif ref_memory_space is MemorySpace.VMEM:
      message += (
          " To load a scalar from VMEM, load an array first and then extract a"
          " particular element, e.g. ``v = ref[pl.ds(idx, ...)]; v[0]``."
      )
    else:
      message += f" Trying to load a scalar from {ref_memory_space!r}."
    raise NotImplementedError(message)
  if out_aval.ndim == 0:
    if mask is not None:
      raise NotImplementedError("Get does not support masked scalar loads")
    return memref.load(ref, starts)

  if not ctx.lowering_context.needs_layout_passes:
    _check_aval_is_supported("Get", out_aval)
  out_vec_type = ir.VectorType.get(
      out_aval.shape, _dtype_to_ir_type(out_aval.dtype)
  )
  if not ctx.lowering_context.needs_layout_passes:
    return tpu.vector_load(
        out_vec_type, ref, indices=starts, strides=[], mask=mask
    )
  # Load at the full memref rank, keeping integer-indexed dims as size 1,
  # because apply-vector-layout requires the vector rank to match the memref.
  memref_vec_shape = cast(
      Sequence[int],
      [1 if squeeze else s for s, squeeze in zip(sizes, squeeze_dims)],
  )
  memref_vec_type = ir.VectorType.get(
      memref_vec_shape, _dtype_to_ir_type(out_aval.dtype)
  )
  load_val = tpu.vector_load(
      memref_vec_type, ref, indices=starts, strides=[], mask=mask
  )
  return vector.shape_cast(out_vec_type, load_val)


def _load_lowering_rule(
    ctx: sc_lowering.LoweringRuleContext, ref, *args, has_mask, tree
):
  if has_mask:
    *flat_transforms, mask = args
  else:
    flat_transforms, mask = list(args), None
  return sc_lowering._load_lowering_rule(
      ctx, ref, mask, *flat_transforms, tree=tree
  )

