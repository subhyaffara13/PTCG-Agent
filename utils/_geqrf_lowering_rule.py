
def _geqrf_lowering_rule(ctx, operand):
  ts_type = mlir.aval_to_ir_type(ctx.module_context, ctx.avals_out[0])
  r_type = mlir.aval_to_ir_type(ctx.module_context, ctx.avals_out[1])
  result_types = [ts_type, r_type]
  if any(not is_constant_shape(aval_out.shape)
         for aval_out in ctx.avals_out):
    result_shapes = [
        mlir.eval_dynamic_shape_as_tensor(ctx, aval_out.shape)
        for aval_out in ctx.avals_out
    ]
  else:
    result_shapes = None
  op = mlir.custom_call(
      "Qr",
      result_types=result_types,
      operands=[operand],
      api_version=1,
      result_shapes=result_shapes
  )
  return op.results

