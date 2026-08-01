
def _remat3(policy, static_argnums, static_argnames, f, *args, **kwargs):
  args_ft = FlatTree.flatten_static_argnums_argnames(
      args, kwargs, static_argnums, static_argnames)
  avals_ft = args_ft.map(typeof)
  dbg = api_util.debug_info(
      'remat3', f, args, kwargs, static_argnums=static_argnums,
      static_argnames=static_argnames)
  jaxpr_, out_avals_ft = pe.trace_to_jaxpr(f, avals_ft, dbg)
  jaxpr, consts = pe.separate_consts(jaxpr_)
  out_flat = RematTraced(jaxpr, policy)(*consts, *args_ft)
  return out_avals_ft.update(out_flat).unflatten()

