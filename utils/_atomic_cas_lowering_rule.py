
def _atomic_cas_lowering_rule(ctx: lowering.LoweringRuleContext, ptr, cmp, val):
  _, cmp_aval, val_aval = ctx.avals_in
  if isinstance(ptr.type, ir.RankedTensorType):
    ptr_type = ir.RankedTensorType(ptr.type)
    element_type = tt_dialect.PointerType(ptr_type.element_type)
    result_type = ir.RankedTensorType.get(
        ptr_type.shape, element_type.pointee_type, ptr_type.encoding
    )
  else:
    result_type = tt_dialect.PointerType(ptr.type).pointee_type
  return tt_dialect.atomic_cas(
      result_type,
      ptr,
      lowering._ensure_ir_value(cmp, cmp_aval),
      lowering._ensure_ir_value(val, val_aval),
      sem=tt_dialect.MemSemantic.ACQUIRE_RELEASE,
      scope=tt_dialect.MemSyncScope.GPU,
  )

