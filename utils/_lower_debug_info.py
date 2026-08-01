
def _lower_debug_info(hi_jaxpr, out_mut):
  debug_info = hi_jaxpr.debug_info
  if debug_info.arg_names is not None:
    lo_arg_names = tuple(
        name for aval, name in zip(hi_jaxpr.in_aval_qdds, debug_info.arg_names)
        for _ in aval.lo_ty())
    debug_info = debug_info._replace(arg_names=lo_arg_names)
  if debug_info.result_paths is not None:
    qdd_paths = ('',) * sum(len(o) for o in out_mut)
    lo_result_paths = tuple(
        path for aval, path in zip(hi_jaxpr.out_avals, debug_info.result_paths)
        for _ in aval.lo_ty())
    debug_info = debug_info._replace(result_paths=(*qdd_paths, *lo_result_paths))
  return debug_info

