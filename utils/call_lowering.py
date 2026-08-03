from typing import Any

def call_lowering(fn_name, call_jaxpr: core.ClosedJaxpr, backend,
                  ctx: ModuleContext, in_avals,
                  out_avals, tokens_in, *args,
                  dim_var_values: Sequence[ir.Value],
                  const_lowering: dict[tuple[int, core.AbstractValue], IrValues],
                  arg_names=None, result_names=None,
                  attributes: None | dict[str, Any] = None):
  assert isinstance(call_jaxpr, core.ClosedJaxpr), type(call_jaxpr)
  const_args_and_avals = core.jaxpr_const_args(call_jaxpr.jaxpr)
  const_args, const_avals = util.unzip2(const_args_and_avals)
  const_arg_values = [ir_constants(c, const_lowering=const_lowering, aval=aval)
                      for c, aval in const_args_and_avals]
  args = tuple(const_arg_values) + args
  if arg_names is not None:
    arg_names = [""] * len(const_args) + arg_names
  in_avals = (*const_avals, *in_avals)

  func_op, output_types, effects = lower_called_computation(
      fn_name, call_jaxpr, ctx, len(const_args), in_avals, out_avals,
      tokens_in,
      backend=backend, arg_names=arg_names, result_names=result_names)
  symbol_name = func_op.name.value
  flat_output_types, treedef = ir_tree_registry.flatten(output_types)
  tokens = [tokens_in.get(eff) for eff in effects]
  args = (*dim_var_values, *tokens, *args)
  flat_args, _ = ir_tree_registry.flatten(args)
  call = func_dialect.CallOp(flat_output_types,
                             ir.FlatSymbolRefAttr.get(symbol_name),
                             flat_args)
  if attributes:
    call.operation.attributes['mhlo.frontend_attributes'] = ir.DictAttr.get(attributes)
  out_nodes = treedef.unflatten(call.results)
  tokens, out_nodes = util.split_list(out_nodes, [len(effects)])
  tokens_out = tokens_in.update_tokens(TokenSet(dict(zip(effects, tokens))))
  return out_nodes, tokens_out

