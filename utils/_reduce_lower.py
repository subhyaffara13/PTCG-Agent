
def _reduce_lower(ctx: mlir.LoweringRuleContext, *values,
                  computation, jaxpr: core.ClosedJaxpr, dimensions):
  assert all(isinstance(x, core.ShapedArray) for x in ctx.avals_in), ctx.avals_in
  operands, init_values = util.split_list(values, [len(values) // 2])
  init_value_avals = ctx.avals_in[len(values) // 2:]
  flat_out_types, _ = mlir.ir_tree_registry.flatten(
      map(partial(mlir.aval_to_ir_types, ctx.module_context), ctx.avals_out))
  op = hlo.ReduceOp(flat_out_types,
                    operands, init_values, mlir.dense_int_array(dimensions))
  ir_types, _ = mlir.ir_tree_registry.flatten(
      map(partial(mlir.aval_to_ir_types, ctx.module_context), init_value_avals))
  reducer = op.regions[0].blocks.append(*(ir_types + ir_types))
  with ir.InsertionPoint(reducer):
    name_stack = source_info_util.new_name_stack()
    if jaxpr.effects:
      raise NotImplementedError('Cannot lower effectful `reduce`.')
    out_nodes, _ = mlir.jaxpr_subcomp(ctx.module_context, jaxpr.jaxpr,
                                      name_stack, mlir.TokenSet(),
                                      jaxpr.consts,
                                      *reducer.arguments,
                                      dim_var_values=ctx.dim_var_values,
                                      const_lowering=ctx.const_lowering,
                                      outer_traceback=ctx.traceback)
    flat_out_nodes, _ = mlir.ir_tree_registry.flatten(out_nodes)
    hlo.return_(flat_out_nodes)
  return [mlir.lower_with_sharding_in_types(ctx, r, aval)
          for r, aval in safe_zip(op.results, ctx.avals_out)]

