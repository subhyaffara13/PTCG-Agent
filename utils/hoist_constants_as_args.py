
def hoist_constants_as_args(
    closed_jaxpr: core.ClosedJaxpr, global_in_avals, in_shardings, in_layouts,
    donated_invars, kept_var_idx: set[int], inout_aliases, mut,
    all_args_info: AllArgsInfo):
  const_args, const_arg_avals = unzip2(
      core.jaxpr_const_args(closed_jaxpr.jaxpr)
  )
  num_const_args = len(const_args)
  if num_const_args:
    global_in_avals = list(const_arg_avals) + global_in_avals
    ca_shardings = pjit.const_args_shardings(const_args)
    in_shardings = (*ca_shardings, *in_shardings)
    ca_layouts = pjit.const_args_layouts(const_args, const_arg_avals,
                                          ca_shardings)
    in_layouts = (*ca_layouts, *in_layouts)

    donated_invars = (False,) * num_const_args + donated_invars
    kept_var_idx = set(range(num_const_args)).union(
        {kv + num_const_args for kv in kept_var_idx})
    if inout_aliases is not None:
      inout_aliases = (None,) * num_const_args + inout_aliases
    if mut is not None:
      mut = MutationData(
          in_mut=mut.in_mut,
          out_mut=[None if i_idx is None else i_idx + num_const_args
                   for i_idx in mut.out_mut])
    if all_args_info.debug_info.arg_names is None:
      arg_names = None
    else:
      arg_names = (("",) * num_const_args + all_args_info.debug_info.arg_names)
    all_args_info = AllArgsInfo(
        [*const_arg_avals, *all_args_info.in_avals],
        all_args_info.debug_info._replace(arg_names=arg_names))

  return (const_args, global_in_avals, in_shardings, in_layouts, donated_invars,
          kept_var_idx, inout_aliases, mut, all_args_info)

