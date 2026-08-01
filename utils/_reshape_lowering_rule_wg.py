
def _reshape_lowering_rule_wg(
    ctx: LoweringRuleContext, x, new_sizes, dimensions, sharding
):
  if dimensions is not None:
    raise NotImplementedError("Not implemented: dimensions")
  if sharding is not None:
    raise NotImplementedError("Not implemented: sharding")
  [x_aval] = ctx.avals_in
  x = _ensure_ir_value(x, x_aval.dtype)
  if x_aval.ndim == 0:  # scalar
    res_ty = ir.VectorType.get(new_sizes, x.type)
    return vector_dialect.broadcast(res_ty, x)
  else:
    res_ty = ir.VectorType.get(new_sizes, ir.VectorType(x.type).element_type)
    return vector_dialect.shape_cast(res_ty, x)

