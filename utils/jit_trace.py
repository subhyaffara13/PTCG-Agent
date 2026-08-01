
def jit_trace(jit_func, *args, **kwargs) -> stages.Traced:
  p, args_flat = _infer_params(jit_func._fun, jit_func._jit_info, args, kwargs)
  arg_types = map(convert_to_metaty, args_flat)
  return stages.Traced(arg_types, p.params, p.in_tree, p.out_tree, p.consts)

