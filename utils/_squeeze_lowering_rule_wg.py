
def _squeeze_lowering_rule_wg(ctx: LoweringRuleContext, x, dimensions):
  [x_aval] = ctx.avals_in
  [y_aval] = ctx.avals_out
  x = _ensure_ir_value(x, x_aval.dtype)
  if y_aval.ndim == 0:  # scalar
    return vector_dialect.extract(
        x, dynamic_position=[], static_position=[0] * x_aval.ndim
    )
  else:
    res_ty = ir.VectorType.get(y_aval.shape, ir.VectorType(x.type).element_type)
    return vector_dialect.shape_cast(res_ty, x)

