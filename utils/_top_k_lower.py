
def _top_k_lower(ctx, operand, k, axis):
  # Move axis to last dimension:
  ndim = len(ctx.avals_in[0].shape)
  if axis != ndim - 1:
    perm = list(range(ndim))
    perm[axis], perm[-1] = perm[-1], perm[axis]
    operand = hlo.transpose(operand, mlir.dense_int_array(perm))
  else:
    perm = None

  # Compute the top-k along the last dimension
  if core.is_constant_dim(k):
    results = chlo.top_k(operand, mlir.i64_attr(k))
  else:
    k_value, = mlir.eval_dynamic_shape_as_vals(ctx, (k,))
    out_values_aval, out_indices_aval, = ctx.avals_out
    flat_result_types, _ = mlir.ir_tree_registry.flatten([
        mlir.aval_to_ir_types(ctx.module_context, out_values_aval),
        mlir.aval_to_ir_types(ctx.module_context, out_indices_aval)
    ])
    results = mlir.custom_call(
        "stablehlo.dynamic_top_k",
        result_types=flat_result_types,
        operands=[operand, k_value],
    ).results

  results = [mlir.lower_with_sharding_in_types(ctx, r, aval)
             for r, aval in zip(results, ctx.avals_out)]
  # Move last dimension back into place
  if perm is not None:
    results = [hlo.transpose(result, mlir.dense_int_array(perm))
               for result in results]
  return results

