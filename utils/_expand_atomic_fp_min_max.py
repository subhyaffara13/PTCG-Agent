
def _expand_atomic_fp_min_max(
  atomic_type: AtomicOpType,
  ptr: ir.Value,
  val: ir.Value,
  mask: ir.Value | None = None,
  semantic: tt_dialect.MemSemantic = tt_dialect.MemSemantic.ACQUIRE_RELEASE,
  sync_scope: tt_dialect.MemSyncScope = tt_dialect.MemSyncScope.GPU,
) -> ir.Value:
  """
  Expands floating point min/max via sequence of integer min/max. Does not handle NaNs.

  min:
     return atomic_smin(i_ptr, i_val) if i_val >= 0 else atomic_umax(i_ptr, i_val)

  max:
     return atomic_smax(i_ptr, i_val) if i_val >= 0 else atomic_umin(i_ptr, i_val)

  """

  if isinstance(ptr.type, ir.RankedTensorType):
    ptr_type = ir.RankedTensorType(ptr.type)
    element_type = tt_dialect.PointerType(ptr_type.element_type)
    result_type = ir.RankedTensorType.get(
      ptr_type.shape, element_type.pointee_type, ptr_type.encoding
    )
  else:
    result_type = tt_dialect.PointerType(ptr.type).pointee_type

  ptr_cast = tt_dialect.bitcast(lowering._fp_bits_type(ptr.type), ptr)
  val_cast = tt_dialect.bitcast(lowering._fp_bits_type(val.type), val)

  zero = lowering._full(val_cast.type, 0)
  pos_cmp = lowering._greater_equal(val_cast, zero, signed=True)
  neg_cmp = lowering._less_than(val_cast, zero, signed=True)

  pos_mask = pos_cmp if mask is None else arith_dialect.andi(mask, pos_cmp)
  neg_mask = neg_cmp if mask is None else arith_dialect.andi(mask, neg_cmp)

  pos_op, neg_op = (
    (tt_dialect.RMWOp.MAX, tt_dialect.RMWOp.UMIN)
    if atomic_type == AtomicOpType.MAX
    else (tt_dialect.RMWOp.MIN, tt_dialect.RMWOp.UMAX)
  )

  pos_val = lowering._atomic_rmw(
    pos_op, ptr_cast, val_cast, mask=pos_mask, semantic=semantic, sync_scope=sync_scope
  )
  neg_val = lowering._atomic_rmw(
    neg_op, ptr_cast, val_cast, mask=neg_mask, semantic=semantic, sync_scope=sync_scope
  )
  result = arith_dialect.select(pos_cmp, pos_val, neg_val)
  return tt_dialect.bitcast(result_type, result)

