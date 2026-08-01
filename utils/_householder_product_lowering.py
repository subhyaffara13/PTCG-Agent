
def _householder_product_lowering(ctx, a, taus):
  aval_out, = ctx.avals_out
  if not is_constant_shape(aval_out.shape):
    result_shapes = [
        mlir.eval_dynamic_shape_as_tensor(ctx, aval_out.shape)]
  else:
    result_shapes = None
  flat_res_types, _ = mlir.ir_tree_registry.flatten(
      mlir.aval_to_ir_types(ctx.module_context, aval_out))
  op = mlir.custom_call(
      "ProductOfElementaryHouseholderReflectors",
      result_types=flat_res_types,
      operands=[a, taus],
      api_version=1,
      result_shapes=result_shapes)
  return [op.result]

