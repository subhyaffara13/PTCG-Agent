
def _select_and_scatter_lower(
    ctx: mlir.LoweringRuleContext, operand, source, init_value, *,
    select_jaxpr: core.Jaxpr, select_consts,
    scatter_jaxpr: core.Jaxpr, scatter_consts, window_dimensions,
    window_strides, padding):
  operand_aval, source_aval, init_value_aval = ctx.avals_in
  aval_out, = ctx.avals_out
  assert isinstance(operand_aval, ShapedArray)
  scalar_aval = operand_aval.update(
      shape=(), sharding=operand_aval.sharding.update(spec=()))
  scalar_type = mlir.aval_to_ir_type(ctx.module_context, scalar_aval)
  result_type = mlir.aval_to_ir_type(ctx.module_context, aval_out)
  op = hlo.SelectAndScatterOp(
      result_type,
      operand,
      source,
      init_value,
      window_dimensions=mlir.dense_int_array(window_dimensions),
      window_strides=mlir.dense_int_array(window_strides),
      padding=ir.DenseIntElementsAttr.get(np.asarray(padding, np.int64),
                                          shape=(len(padding), 2)))
  select = op.select.blocks.append(scalar_type, scalar_type)
  with ir.InsertionPoint(select):
    if select_jaxpr.effects:
      raise NotImplementedError('Cannot lower effectful `select`.')
    out_nodes, _ = mlir.jaxpr_subcomp(ctx.module_context, select_jaxpr,
                                      ctx.name_stack,
                                      mlir.TokenSet(), select_consts,
                                      *select.arguments,
                                      dim_var_values=ctx.dim_var_values,
                                      const_lowering=ctx.const_lowering,
                                      outer_traceback=ctx.traceback)
    flat_out_nodes, _ = mlir.ir_tree_registry.flatten(out_nodes)
    hlo.return_(flat_out_nodes)
  scatter = op.scatter.blocks.append(scalar_type, scalar_type)
  with ir.InsertionPoint(scatter):
    if scatter_jaxpr.effects:
      raise NotImplementedError('Cannot lower effectful `scatter`.')
    out_nodes, _ = mlir.jaxpr_subcomp(ctx.module_context, scatter_jaxpr,
                                      ctx.name_stack,
                                      mlir.TokenSet(), scatter_consts,
                                      *scatter.arguments,
                                      dim_var_values=ctx.dim_var_values,
                                      const_lowering=ctx.const_lowering,
                                      outer_traceback=ctx.traceback)
    flat_out_nodes, _ = mlir.ir_tree_registry.flatten(out_nodes)
    hlo.return_(flat_out_nodes)
  return [mlir.lower_with_sharding_in_types(ctx, r, aval)
          for r, aval in zip(op.results, ctx.avals_out)]

