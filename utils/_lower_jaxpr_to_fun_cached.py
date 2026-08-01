
def _lower_jaxpr_to_fun_cached(
    ctx: ModuleContext, fn_name, call_jaxpr: core.ClosedJaxpr,
    num_const_args: int, effects, in_avals, arg_names=None, result_names=None):
  assert num_const_args + len(call_jaxpr.in_avals) == len(in_avals)
  if not call_jaxpr.consts and arg_names is result_names is None:
    # Cacheable.
    key = (fn_name, call_jaxpr.jaxpr, tuple(effects))
    try:
      func_op = ctx.cached_primitive_lowerings[key]
    except KeyError:
      func_op = lower_jaxpr_to_fun(
          ctx, fn_name, call_jaxpr, effects, num_const_args=num_const_args,
          in_avals=in_avals, arg_names=arg_names, result_names=result_names)
      ctx.cached_primitive_lowerings[key] = func_op
  else:
    func_op = lower_jaxpr_to_fun(
        ctx, fn_name, call_jaxpr, effects,
        num_const_args=num_const_args, in_avals=in_avals,
        arg_names=arg_names, result_names=result_names)
  return func_op

