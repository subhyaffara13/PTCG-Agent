
def _masked_swap_lowering_rule(
    ctx: LoweringRuleContext, *args_flat, args_tree, **_
):
  ref, transforms, val, mask = args_tree.unflatten(args_flat)
  ref_aval, transforms_avals, val_aval, mask_aval = args_tree.unflatten(
      ctx.avals_in
  )
  prev_transforms, idx = _canonicalize_transforms_to_indexer(
      ref_aval, transforms, transforms_avals
  )

  if mask is not None:
    if  val_aval.dtype.itemsize != 4:
      raise NotImplementedError("masked swap with non-32-bit data")
    if val_aval.shape != mask_aval.shape:
      raise ValueError(
          "Expected value and mask to have the same shape, but got"
          f" value shape {val_aval.shape} vs. mask shape {mask_aval.shape}."
      )

  ref_block_shape, *_ = ctx.block_shapes
  ref, ref_block_shape = _transform_ref(
      ref, ref_aval, ref_block_shape, prev_transforms
  )

  ref_type = ir.MemRefType(ref.type)
  memory_space = str(ref_type.memory_space)
  is_smem_store = memory_space == "#tpu.memory_space<smem>"
  is_vmem_store = memory_space == "#tpu.memory_space<vmem>"
  (aval_out,) = ctx.avals_out
  if not isinstance(val, ir.Value):
    val = ir_constant(val, mlir_type=_dtype_to_ir_type(val_aval.dtype))
  if not is_smem_store and not ref_block_shape:
    raise NotImplementedError(
        "Indexing into a ()-shaped Ref not yet supported on TPU.")

  starts, _, strides, _, _ = _indexer_to_start_size_stride(
      idx,
      ref_block_shape,
      cast_to_index=True,
  )
  need_stride = not all((s is None or s == 1) for s in strides)

  if is_smem_store:
    if mask is not None:
      raise ValueError("SMEM store does not support masks")
    if val_aval.shape:
      raise ValueError("Can only store scalars to SMEM")
    result = memref.load(ref, starts)
    result = _maybe_cast_load_to_bool(ctx, val_aval, result)
    val = _maybe_cast_store_to_memref_type(ctx, val_aval, val)
    memref.store(val, ref, starts)
    return result

  if not is_vmem_store:
    extra = ""
    if memory_space == "#tpu.memory_space<any>":
      extra = " ANY memory space can only be accessed using async_copy."
    raise ValueError(
        "Loads and stores are only allowed on VMEM and SMEM references." + extra
    )

  # handling VMEM store below
  if not val_aval.shape:
    raise ValueError("Cannot store scalars to VMEM")

  mem_slice_shape = list(aval_out.shape)
  for i, a in enumerate(idx.indices):
    if not isinstance(a, primitives.Slice):
      mem_slice_shape.insert(i, 1)
  mem_slice_shape_iter = iter(mem_slice_shape)
  mem_slice_shape = [
      1 if b is pallas_core.squeezed else next(mem_slice_shape_iter)
      for b in ref_block_shape
  ]
  mem_aval = aval_out.update(
      shape=tuple(mem_slice_shape), sharding=jax_core.get_cur_mesh_sharding()
  )
  mem_aval_vec_type = ir.VectorType.get(
      ctx.lowering_context.dynamic_shape_replacement_fn(mem_aval.shape),
      _dtype_to_ir_type(mem_aval.dtype, is_kernel_boundary=True)
  )
  if need_stride:
    result = tpu.strided_load(mem_aval_vec_type, ref, starts, strides)
  else:
    result = vector.load(mem_aval_vec_type, ref, starts)
  val = _maybe_cast_store_to_memref_type(ctx, val_aval, val)
  if mem_aval != aval_out:
    if not aval_out.shape:
      raise ValueError("Cannot swap scalars to VMEM.")
    # We are slicing a scalar so provided dummy 1 indices
    result_vec_type = ir.VectorType.get(
        ctx.lowering_context.dynamic_shape_replacement_fn(aval_out.shape),
      _dtype_to_ir_type(aval_out.dtype, is_kernel_boundary=True))
    result = vector.shape_cast(result_vec_type, result)
    val_vec_type = ir.VectorType.get(
        ctx.lowering_context.dynamic_shape_replacement_fn(mem_aval.shape),
      _dtype_to_ir_type(mem_aval.dtype, is_kernel_boundary=True))
    val = vector.shape_cast(val_vec_type, val)
    if mask is not None:
      mask_vec_type = ir.VectorType.get(
          ctx.lowering_context.dynamic_shape_replacement_fn(mem_aval.shape),
          _dtype_to_ir_type(mask_aval.dtype)
      )
      mask = vector.shape_cast(mask_vec_type, mask)
  result = _maybe_cast_load_to_bool(ctx, val_aval, result)

  if need_stride:
    if mask is not None:
      raise NotImplementedError("masked swap with strided store")
    tpu.strided_store(val, ref, starts, strides)
  else:
    tpu.vector_store(val, ref, starts, strides=[], mask=mask)
  return result


def _masked_swap_lowering_rule(
    ctx: LoweringRuleContext, *args_flat, args_tree, eviction_policy
):
  block_info, *_ = ctx.block_infos
  assert block_info is not None
  ptr, indexers, value, mask = args_tree.unflatten(args_flat)
  ref_aval, _, value_aval, mask_aval = args_tree.unflatten(ctx.avals_in)
  if len(indexers) > 1:
    raise NotImplementedError("No support for multiple indexers yet.")
  if not indexers:
    idx = NDIndexer.make_trivial_indexer(ref_aval.shape)
  else:
    idx = indexers[0]
  ptr = _compute_pointers_from_indices(ptr, block_info, idx)
  other = None
  if value is not None:
    value = _ensure_ir_value(value, value_aval)
  if mask is not None:
    shape = idx.get_indexer_shape_static()
    mask = _bcast_to(_ensure_ir_value(mask, mask_aval), shape)
    if value is not None:
      other = _bcast_to(value, shape)

  old_value = _load(ptr, mask=mask, other=other)
  _store(ptr, value, mask=mask, eviction_policy=eviction_policy)  # pyrefly: ignore[bad-argument-type]
  return old_value

