
def _lower_create_linear(ctx):
  out_aval, = ctx.avals_out
  flat_res_types, _ = mlir.ir_tree_registry.flatten(mlir.aval_to_ir_types(ctx.module_context, out_aval))
  return mlir.custom_call(
      "CreateBuffer",
      operands=[],
      result_types=flat_res_types,
  ).results

