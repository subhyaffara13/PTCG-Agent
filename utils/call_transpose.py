
def call_transpose(primitive, params, call_jaxpr: core.Jaxpr, args, ct, _):
  if isinstance(call_jaxpr, core.ClosedJaxpr):
    call_jaxpr, consts = call_jaxpr.jaxpr, call_jaxpr.consts
  else:
    consts = ()
  all_args, in_treedef = tree_flatten((consts, args, ct))
  fun = lu.hashable_partial(
      lu.wrap_init(backward_pass, debug_info=call_jaxpr.debug_info),
      call_jaxpr, False)
  fun, out_tree = flatten_fun_nokwargs(fun, in_treedef)
  update_params = call_transpose_param_updaters.get(primitive)
  if update_params:
    params = update_params(params, map(is_undefined_primal, args),
                           [type(x) is not Zero for x in ct])
  out_flat = primitive.bind(*all_args, **dict(params, subfuns=(fun,)))
  return tree_unflatten(out_tree(), out_flat)

