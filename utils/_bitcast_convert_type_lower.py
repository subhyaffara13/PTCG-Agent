
def _bitcast_convert_type_lower(ctx, operand, *, new_dtype):
  aval_out, = ctx.avals_out
  out_type = mlir.aval_to_ir_type(ctx.module_context, aval_out)
  out = hlo.bitcast_convert(out_type, operand)
  return [mlir.lower_with_sharding_in_types(ctx, out, aval_out)]

