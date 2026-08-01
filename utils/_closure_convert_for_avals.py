
def _closure_convert_for_avals(fun, in_tree, in_avals,
                               debug_info: core.DebugInfo):
  wrapped_fun, out_tree = flatten_fun_nokwargs(
      lu.wrap_init(fun, debug_info=debug_info), in_tree)
  jaxpr, out_pvals, consts = pe.trace_to_jaxpr_dynamic(wrapped_fun, in_avals)
  out_tree = out_tree()

  (closure_consts, const_args), merge = partition_list(_maybe_perturbed, consts)
  num_consts = len(const_args)

  def converted_fun(*args_hconsts):
    num_args = len(args_hconsts) - num_consts
    args, const_args = split_list(args_hconsts, [num_args])
    consts = merge(closure_consts, const_args)
    all_args, in_tree2 = tree_flatten(tuple(args))
    if in_tree != in_tree2:
      msg = ("The inputs to the closure produced by closure_convert must have "
             "the same Pytree structure as the example arguments passed when "
             f"closure_convert was called. Expected {in_tree}, but got "
             f"{in_tree2}")
      raise TypeError(msg)
    out_flat = core.eval_jaxpr(jaxpr, consts, *all_args)
    return tree_unflatten(out_tree, out_flat)

  return converted_fun, const_args

