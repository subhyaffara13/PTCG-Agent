
def lower_called_computation(
    fn_name, call_jaxpr: core.ClosedJaxpr, ctx: ModuleContext,
    num_const_args: int, in_avals, out_avals, tokens_in, backend=None,
    arg_names=None, result_names=None):
  assert isinstance(call_jaxpr, core.ClosedJaxpr), type(call_jaxpr)
  check_backend_matches(backend, ctx.platforms)
  effects = list(tokens_in.effects())
  output_types = [_aval_to_ir_types(ctx, a) for a in out_avals]
  output_types = [token_type()] * len(effects) + output_types
  func_op = _lower_jaxpr_to_fun_cached(
      ctx, fn_name, call_jaxpr, num_const_args, effects, in_avals=in_avals,
      arg_names=arg_names, result_names=result_names)
  return func_op, output_types, effects

