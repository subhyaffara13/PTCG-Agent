
def _atomic_lowering_rule(
    ctx: lowering.LoweringRuleContext,
    *args_flat,
    args_tree,
    atomic_type: AtomicOpType,
):
  block_info, *_ = ctx.block_infos
  assert block_info is not None
  ptr, indexers, val, mask = args_tree.unflatten(args_flat)
  *_, value_aval, mask_aval = args_tree.unflatten(ctx.avals_in)
  indexers = list(indexers)
  if not indexers or not isinstance(indexers[-1], indexing.NDIndexer):
    ref_aval = state.transform_type(indexers, ctx.avals_in[0])
    assert isinstance(ref_aval, state.AbstractRef)
    indexers.append(indexing.NDIndexer.make_trivial_indexer(ref_aval.shape))
  if len(indexers) != 1:
    raise NotImplementedError("Only single indexer is supported.")
  idx = indexers[0]
  ptr = lowering._compute_pointers_from_indices(ptr, block_info, idx)
  val = lowering._ensure_ir_value(val, value_aval)
  if mask is not None:
    mask = lowering._ensure_ir_value(mask, mask_aval)
  if atomic_type == AtomicOpType.XCHG:
    op = tt_dialect.RMWOp.XCHG
  elif atomic_type == AtomicOpType.ADD:
    if isinstance(val.type, ir.IntegerType):
      op = tt_dialect.RMWOp.ADD
    else:
      op = tt_dialect.RMWOp.FADD
  elif atomic_type == AtomicOpType.MIN:
    if isinstance(val.type, ir.IntegerType):
      op = (
        tt_dialect.RMWOp.MIN
        if jnp.issubdtype(value_aval.dtype, jnp.signedinteger)
        else tt_dialect.RMWOp.UMIN
      )
    else:
      return _expand_atomic_fp_min_max(atomic_type, ptr, val, mask=mask)
  elif atomic_type == AtomicOpType.MAX:
    if isinstance(val.type, ir.IntegerType):
      op = (
        tt_dialect.RMWOp.MAX
        if jnp.issubdtype(value_aval.dtype, jnp.signedinteger)
        else tt_dialect.RMWOp.UMAX
      )
    else:
      return _expand_atomic_fp_min_max(atomic_type, ptr, val, mask=mask)
  elif atomic_type == AtomicOpType.AND:
    op = tt_dialect.RMWOp.AND
  elif atomic_type == AtomicOpType.OR:
    op = tt_dialect.RMWOp.OR
  elif atomic_type == AtomicOpType.XOR:
    op = tt_dialect.RMWOp.XOR
  else:
    raise NotImplementedError(f"unsupported atomic operation: {atomic_type}")
  return lowering._atomic_rmw(op, ptr, val, mask=mask)

