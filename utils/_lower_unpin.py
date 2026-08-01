
def _lower_unpin(ctx, x_op):
  out_aval, = ctx.avals_out
  flat_ops, _ = mlir.ir_tree_registry.flatten([x_op])
  flat_res_types, _ = mlir.ir_tree_registry.flatten(mlir.aval_to_ir_types(ctx.module_context, out_aval))
  return mlir.custom_call(
      "Unpin",
      operands=flat_ops,
      result_types=flat_res_types,
  ).results

