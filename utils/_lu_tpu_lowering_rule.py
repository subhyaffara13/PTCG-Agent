
def _lu_tpu_lowering_rule(ctx, operand):
  result_types, _ = mlir.ir_tree_registry.flatten([
      mlir.aval_to_ir_types(ctx.module_context, ctx.avals_out[0]),
      mlir.aval_to_ir_types(ctx.module_context, ctx.avals_out[1]),
      mlir.aval_to_ir_types(ctx.module_context, ctx.avals_out[2]),
  ])
  if any(not is_constant_shape(a.shape) for a in ctx.avals_out):
    result_shapes = [
      mlir.eval_dynamic_shape_as_tensor(ctx, a.shape)
      for a in ctx.avals_out]
  else:
    result_shapes = None
  op = mlir.custom_call(
    "LuDecomposition",
    result_types=result_types,
    operands=[operand],
    result_shapes=result_shapes)
  return op.results

