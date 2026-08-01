
def _broadcast_in_dim_lowering_rule_wg(
    ctx: LoweringRuleContext,
    x,
    *,
    broadcast_dimensions,
    shape,
    sharding,
):
  del sharding
  [x_aval] = ctx.avals_in
  mlir_type = mgpu_utils.dtype_to_ir_type(x_aval.dtype)
  result_ty = ir.VectorType.get(shape, mlir_type)
  if not broadcast_dimensions:
    # Even though we could implement this case by passing a 0D vector as input
    # to mgpu.dialect.BroadcastInDimOp we don't want that. 0D vectors are
    # generally problematic and so we avoid them by specializing that case
    # directly here.
    x = _ensure_ir_value(x, x_aval.dtype)
    return vector_dialect.broadcast(result_ty, x)
  return mgpu.dialect.broadcast_in_dim(result_ty, x, broadcast_dimensions)

