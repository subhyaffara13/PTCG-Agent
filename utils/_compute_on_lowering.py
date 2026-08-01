
def _compute_on_lowering(ctx, *args, jaxpr, compute_type, out_memory_spaces,
                         compiler_options_json):
  if dispatch.jaxpr_has_primitive(jaxpr, 'compute_on'):
    raise ValueError("Nesting `compute_on` with different compute types is "
                     "not allowed.")
  const_args_and_avals = core.jaxpr_const_args(jaxpr.jaxpr)
  const_args, const_avals = unzip2(const_args_and_avals)
  const_arg_values = [
      mlir.ir_constants(c, const_lowering=ctx.const_lowering, aval=aval)
      for c, aval in const_args_and_avals]
  in_avals = (*const_avals, *ctx.avals_in)
  func_op, output_types, effects = mlir.lower_called_computation(
      "compute_on", jaxpr, ctx.module_context, len(const_args), in_avals,
      ctx.avals_out, ctx.tokens_in)

  symbol_name = func_op.name.value
  flat_output_types, treedef = mlir.ir_tree_registry.flatten(output_types)
  tokens = [ctx.tokens_in.get(eff) for eff in effects]
  args = (*ctx.dim_var_values, *tokens, *const_arg_values, *args)
  flat_args, _ = mlir.ir_tree_registry.flatten(args)
  call = func_dialect.CallOp(
      flat_output_types, ir.FlatSymbolRefAttr.get(symbol_name),
      flat_args)

  if compute_type.startswith("gpu_stream:"):
    dict_attr = {
        "_xla_stream_annotation": ir.StringAttr.get(compute_type.split(":")[1]),
        "inlineable": ir.StringAttr.get("false"),
    }
  else:
    ctype = mlir.map_compute_type(compute_type)
    dict_attr = {"_xla_compute_type": ir.StringAttr.get(ctype)}

  if compiler_options_json is not None:
    dict_attr |= {'backend_config': ir.StringAttr.get(compiler_options_json)}
  elif compute_type == 'device':
    dict_attr |= {'inlineable': ir.StringAttr.get('false')}

  call.operation.attributes['mhlo.frontend_attributes'] = ir.DictAttr.get(dict_attr)  # type: ignore

  out_nodes = treedef.unflatten(call.results)
  tokens, out_nodes = split_list(out_nodes, [len(effects)])
  tokens_out = ctx.tokens_in.update_tokens(mlir.TokenSet(dict(zip(effects, tokens))))
  ctx.set_tokens_out(tokens_out)
  return [
      mlir.wrap_with_memory_kind(ctx.module_context, on, core.mem_space_to_kind(oms), out_aval)  # pyrefly: ignore[bad-argument-type]
      for on, out_aval, oms in zip(out_nodes, ctx.avals_out, out_memory_spaces)
  ]

