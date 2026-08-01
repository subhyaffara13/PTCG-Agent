
def _xla_metadata_call_lowering(ctx, *args, jaxpr, **meta):
  const_args_and_avals = core.jaxpr_const_args(jaxpr.jaxpr)
  const_args, const_avals = unzip2(const_args_and_avals)
  in_avals = (*const_avals, *jaxpr.in_avals)
  func_op, output_types, effects = mlir.lower_called_computation(
      "xla_metadata_call", jaxpr, ctx.module_context, len(const_args), in_avals,
      ctx.avals_out, ctx.tokens_in)

  symbol_name = func_op.name.value
  flat_output_types, treedef = mlir.ir_tree_registry.flatten(output_types)
  tokens = [ctx.tokens_in.get(eff) for eff in effects]
  hoisted_const_values, _ = mlir.ir_tree_registry.flatten([
      mlir.ir_constants(c, const_lowering=ctx.const_lowering, aval=aval)
      for c, aval in const_args_and_avals
  ])
  args = (*ctx.dim_var_values, *tokens, *hoisted_const_values, *args)
  flat_args, _ = mlir.ir_tree_registry.flatten(args)
  call = func_dialect.CallOp(
      flat_output_types, ir.FlatSymbolRefAttr.get(symbol_name),
      flat_args)
  call.operation.attributes['mhlo.frontend_attributes'] = ir.DictAttr.get(
      {k: attr_get(v) for k, v in meta.items()})
  out_nodes = treedef.unflatten(call.results)
  tokens, out_nodes = split_list(out_nodes, [len(effects)])
  tokens_out = ctx.tokens_in.update_tokens(mlir.TokenSet(dict(zip(effects, tokens))))
  ctx.set_tokens_out(tokens_out)
  return out_nodes

