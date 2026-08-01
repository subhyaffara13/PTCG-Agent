
def _approx_top_k_lowering(ctx, operand, *, k,
                                  reduction_dimension, recall_target, is_max_k,
                                  reduction_input_size_override,
                                  aggregate_to_topk, fallback=False):
  assert ctx.avals_in
  assert all(isinstance(x, core.ShapedArray) for x in ctx.avals_in)

  op_shape = ctx.avals_in[0].shape
  if len(op_shape) == 0:
    raise ValueError(f'operand must be an array, but was {op_shape}')

  op_dims = op_shape
  op_type = mlir.dtype_to_ir_type(ctx.avals_in[0].dtype)
  recall_type = ir.F32Type.get()
  if reduction_dimension < 0:
    reduction_dimension = len(op_dims) + reduction_dimension

  comparator = _comparator_builder_mlir(ctx, op_type, is_max_k)
  iota = mlir.iota(ctx, core.ShapedArray(ctx.avals_in[0].shape, np.int32),
                   dimension=reduction_dimension)

  init_arg = hlo.constant(ir.DenseElementsAttr.get(np.int32(-1)))
  init_val_array = _get_init_val_literal(ctx.avals_in[0].dtype, is_max_k)
  init_vals = [mlir.ir_constant(init_val_array.reshape(()))]

  backend_config = {
    "reduction_dim" : mlir.i64_attr(reduction_dimension),
    "recall_target" : mlir.ir.FloatAttr.get(recall_type, recall_target),
    "aggregate_to_topk" : mlir.ir.BoolAttr.get(aggregate_to_topk),
    "reduction_input_size_override" :
      mlir.i64_attr(reduction_input_size_override)}
  if fallback:
    backend_config["is_fallback"] = mlir.ir.BoolAttr.get(fallback)

  if all(core.is_constant_shape(aval_out.shape) for aval_out in ctx.avals_out):
    result_shapes = None
  else:
    result_shapes, _ = mlir.ir_tree_registry.flatten([
        mlir.shape_tensor(ctx.module_context, mlir.eval_dynamic_shape(ctx, aval_out.shape))
        for aval_out in ctx.avals_out
    ])

  flat_res_types, _ = mlir.ir_tree_registry.flatten([
      mlir.aval_to_ir_types(ctx.module_context, a) for a in ctx.avals_out
  ])
  if core.is_constant_dim(k):
    backend_config["top_k"] = mlir.i64_attr(k)
    out = mlir.custom_call(
        "ApproxTopK",
        result_types=flat_res_types,
        operands=[operand, iota, *init_vals, init_arg],
        called_computations=[comparator.name.value],
        backend_config=backend_config,
        result_shapes=result_shapes)
  else:
    k_value, = mlir.eval_dynamic_shape_as_vals(ctx, (k,))
    out = mlir.custom_call(
        "stablehlo.dynamic_approx_top_k",
        result_types=flat_res_types,
        operands=[operand, iota, *init_vals, init_arg, k_value],
        called_computations=[comparator.name.value],
        backend_config=backend_config,
        result_shapes=result_shapes)

  return out.results

