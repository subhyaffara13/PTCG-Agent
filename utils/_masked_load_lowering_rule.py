
def _masked_load_lowering_rule(
    ctx: LoweringRuleContext,
    *args_flat,
    args_tree,
    eviction_policy,
    cache_modifier,
    is_volatile,
):
  block_info, *_ = ctx.block_infos
  assert block_info is not None
  ptr, indexers, mask, other = args_tree.unflatten(args_flat)
  *_, mask_aval, other_aval = args_tree.unflatten(ctx.avals_in)
  if len(indexers) > 1:
    raise NotImplementedError("No support for multiple indexers yet.")
  indexers = list(indexers)
  if not indexers:
    ref_aval = state.transform_type(indexers, ctx.avals_in[0])
    assert isinstance(ref_aval, state.AbstractRef)
    idx = NDIndexer.make_trivial_indexer(ref_aval.shape)
  else:
    idx = indexers[0]
  if not _is_triton_pointer_type(ptr.type):
    assert len(ctx.avals_in) == 1
    return ptr

  is_int4 = block_info.full_shape_dtype.dtype in (jnp.int4, jnp.uint4)
  is_contiguous_int4 = _is_contiguous_int4(block_info, idx)

  if is_contiguous_int4:
    # If the load reads contiguously in the last dimension, we can reinterpret
    # the `int4` block as `uint8`. This generates much more efficient code. The
    # more generic `int4` code below has offsets like `0, 0, 1, 1, ...`, which
    # Triton doesn't optimize as well.
    block_info, idx = _reinterpret_int4_as_uint8(block_info, idx)

  offsets = _compute_offsets_from_indices(block_info, idx)
  ptr_offsets = offsets

  if is_int4 and not is_contiguous_int4:
    ptr_offsets = _floordiv(offsets, _full(offsets.type, 2), signed=False)

  shape = idx.get_indexer_shape_static()
  ptr = _add(_bcast_to(ptr, shape), ptr_offsets)
  if mask is not None:
    mask = _bcast_to(_ensure_ir_value(mask, mask_aval), shape)
  if other is not None:
    other = _bcast_to(_ensure_ir_value(other, other_aval), shape)
  values = _load(
      ptr,
      mask=mask,
      other=other,
      cache_modifier=cache_modifier,
      is_volatile=is_volatile,
      eviction_policy=eviction_policy,
  )

  if not is_int4:
    return values

  if is_contiguous_int4:
    msb_values = arith_dialect.shrui(values, _full(values.type, 4))
    join_type = get_join_type(ir.RankedTensorType(values.type))
    values = tt_dialect.join(join_type, values, msb_values)
    shape = ir.RankedTensorType(values.type).shape
    values = _reshape(values, (*shape[:-2], shape[-2] * shape[-1]))
  else:
    offsets = _ir_cast(offsets, ir.IntegerType.get_signless(32), signed=False)
    in_msb = _mod(offsets, _full(offsets.type, 2), signed=False)
    shift = _mul(in_msb, _full(in_msb.type, 4))
    shift = _ir_cast(shift, values.type, signed=False)
    values = arith_dialect.shrui(values, shift)
  return _ir_cast(values, ir.IntegerType.get_signless(4), signed=False)

