
def _rearrange_mutable_binders(
    jaxpr: ClosedJaxpr, num_prefix: int, num_binders: int
) -> ClosedJaxpr:
  fst, invars, rst = split_list(jaxpr.jaxpr.invars, [num_prefix, num_binders])
  is_mutable = [isinstance(v.aval, AbstractRef) for v in invars]
  immut_invars, mut_invars = partition_list(is_mutable, invars)
  new_invars = [*fst, *mut_invars, *immut_invars, *rst]
  if jaxpr.jaxpr.debug_info.arg_names is None:
    new_arg_names = None
  else:
    fst, names, rst = split_list(jaxpr.jaxpr.debug_info.arg_names,
                                 [num_prefix, num_binders])
    immut_names, mut_names = partition_list(is_mutable, names)
    new_arg_names = [*fst, *mut_names, *immut_names, *rst]
  dbg = jaxpr.jaxpr.debug_info._replace(arg_names=new_arg_names)

  new_jaxpr = jaxpr.jaxpr.replace(invars=new_invars, debug_info=dbg)
  if config.enable_checks.value: core.check_jaxpr(new_jaxpr)
  return ClosedJaxpr(new_jaxpr, jaxpr.consts)

